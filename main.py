import os

from dotenv import load_dotenv

from upload_to_strava import main


load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
DIRECTORY = os.path.join(os.getcwd(), 'data')
FILE_TYPE = '.gpx'  # '.gpx', '.tcx' or '.csv'

SPORT_NAMES = {
    # Endomondo
    'SKIING_CROSS_COUNTRY': 'NordicSki',
    'RUNNING': 'Run',
    'ORIENTEERING': 'Run',
    'WALKING': 'Walk',
    'FITNESS_WALKING': 'Hike',
    'CYCLING_SPORT': 'Ride',
    'CYCLING_TRANSPORTATION': 'Ride',
    'ROLLER_SKATING': 'InlineSkate',
    # Runkeeper
    'Running': 'Run',
    'Cycling': 'Ride',
    'Cross-Country': 'NordicSki',
    'Other': 'Run',
}


if __name__ == '__main__':
    main(ACCESS_TOKEN, DIRECTORY, SPORT_NAMES, FILE_TYPE)

