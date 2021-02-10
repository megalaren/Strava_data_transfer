import os
import time
import csv

import requests

from logger import logger
from parsing_gpx import get_gpx_activity_type
from parsing_json import get_json_activity_type
from parsing_csv import parsing_data_from_csv


URL_CREATE_ACTIVITY = 'https://www.strava.com/api/v3/activities'
URL_UPLOADS = 'https://www.strava.com/api/v3/uploads'
URL_CHECK_UPLOAD_STATUS = 'https://www.strava.com/api/v3/uploads/{upload_id}'


# file and list for saving sent tracks
UPLOADED_FILES = os.path.join(os.getcwd(), 'uploaded_files.txt')
uploaded_files = []
try:
    with open(UPLOADED_FILES, mode='r') as f:
        for line in f:
            if not line.isspace():
                uploaded_files.append(line.replace('\n', ''))
except FileNotFoundError:
    open(UPLOADED_FILES, 'w').close()


def save_uploaded_file_name(file_name):
    """Save uploaded file name to UPLOADED_FILES and uploaded_files."""
    uploaded_files.append(file_name)
    with open(UPLOADED_FILES, mode='a') as file:
        file.write(file_name + '\n')


def get_headers(token):
    return {'Authorization': 'Bearer ' + token}


def error_processing(response, activity_id):
    message = response.get('message')
    if message == 'Rate Limit Exceeded':
        logger.info('The limit of requests to api is exceeded, '
                    'the program falls asleep for 2 minutes')
        time.sleep(120)
    elif message == 'Authorization Error':
        raise TimeoutError(f'Authorization Error. response = \n{response}')
    else:
        logger.error('An unknown error occured while loading activity '
                     f'{activity_id}')
        raise TimeoutError(f'response = \n{response}')


def upload_file(token, file, file_name, activity_type, data_type,
                description=None):
    data = {
        'data_type': data_type,
        'activity_type': activity_type,
        'description': description,
    }
    headers = get_headers(token)

    while True:
        response = requests.post(
            url=URL_UPLOADS,
            files={'file': file},
            headers=headers,
            data=data
        ).json()
        if not response.get('errors'):
            break
        error_processing(response, file_name)
    upload_id = response.get('id')
    status = response.get('status')

    while status != 'Your activity is ready.':
        time.sleep(2)
        response = check_status(upload_id, headers)
        error = response.get('error')
        errors = response.get('errors')
        if errors:
            error_processing(response, file_name)
        if error:
            if 'duplicate of activity' in error:
                logger.error(f'Activity {file_name} already exists')
                break
            logger.error(f'While uploading a {file_name} '
                         f'an error occurred, response =\n{response}')
            break
        status = response.get('status')
    else:
        logger.info(f'Activity {file_name} loaded')


def upload_new_activity(token, data, activity_id):
    headers = get_headers(token)
    while True:
        response = requests.post(
            url=URL_CREATE_ACTIVITY,
            headers=headers,
            data=data
        ).json()
        if response.get('errors'):
            error_processing(response, activity_id)
        elif response.get('error'):
            logger.error(f'In upload_new_activity() while uploading '
                         f'{activity_id} an unknown error:\n{response}')
            break
        elif response.get('message') == 'error':
            logger.error(f'Activity {activity_id} already exists')
            save_uploaded_file_name(activity_id)
            break
        else:
            logger.info(f'Activity {activity_id} loaded')
            save_uploaded_file_name(activity_id)
            break


def check_status(upload_id, headers):
    return requests.get(
        url=URL_CHECK_UPLOAD_STATUS.format(upload_id=upload_id),
        headers=headers,
    ).json()


def send_tcx_file(token, tcx_file_path, file_name, sport_names):
    json_file_path = os.path.splitext(tcx_file_path)[0] + '.json'
    activity_type = get_json_activity_type(json_file_path)
    description = None
    if activity_type in sport_names:
        if activity_type == 'ORIENTEERING':
            description = 'Ориентирование'
        activity_type = sport_names.get(activity_type)
    else:
        raise ValueError(f'{activity_type} is missing in SPORT_NAMES')
    with open(tcx_file_path, 'rb') as tcx_file:
        upload_file(
            token=token,
            file=tcx_file,
            activity_type=activity_type,
            description=description,
            data_type='tcx',
            file_name=file_name,
        )


def send_gpx_file(token, gpx_file_path, file_name, sport_names):
    activity_type = get_gpx_activity_type(gpx_file_path)
    description = None
    if activity_type in sport_names:
        if activity_type == 'Other':
            description = 'Ориентирование'
        activity_type = sport_names.get(activity_type)
    else:
        raise ValueError(f'{activity_type} is missing in SPORT_NAMES')
    with open(gpx_file_path, 'rb') as gpx_file:
        upload_file(
            token=token,
            file=gpx_file,
            activity_type=activity_type,
            description=description,
            data_type='gpx',
            file_name=file_name,
        )


def send_from_csv_file(token, csv_file_path, sport_names):
    with open(csv_file_path, encoding='utf-8') as r_file:
        # Create object DictReader, delimiter-character is ','
        file_reader = csv.DictReader(r_file, delimiter=',')
        for row in file_reader:
            if not row['GPX File']:
                parsing_data = parsing_data_from_csv(row, sport_names)
                data = parsing_data['data']
                activity_id = parsing_data['activity_id']
                if activity_id in uploaded_files:
                    logger.info(
                        f'Activity {activity_id} already in uploaded_files')
                    continue
                upload_new_activity(token, data, activity_id)


def send_file(token, file_name, file_path, file_type, sport_names):
    if file_type == '.gpx':
        send_gpx_file(token, file_path, file_name, sport_names)
    elif file_type == '.tcx':
        send_tcx_file(token, file_path, file_name, sport_names)
    elif file_type == '.csv':
        send_from_csv_file(token, file_path, sport_names)
    else:
        raise ValueError(f'Invalid file type: "{file_type}"\n'
                         f'Expected ".tcx", .gpx" или ".csv"')


def main(token, directory, sport_names, file_type):
    logger.debug('Start program')

    for file_name in os.listdir(directory):
        if not file_name.endswith(file_type):
            continue
        if file_name in uploaded_files:
            logger.info(f'Activity {file_name} already in uploaded_files')
            continue
        file_path = os.path.join(directory, file_name)
        try:
            send_file(token, file_name, file_path, file_type, sport_names)
        except Exception as error:
            logger.error(f'Error in send_file():\n{error}')
            break
        save_uploaded_file_name(file_name)

    logger.debug('The program exits')
