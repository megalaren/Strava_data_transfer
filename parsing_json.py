import os
import json


def get_json_activity_type(json_file_path):
    activity_type = None
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        for elem in json_data:
            if 'sport' in elem:
                activity_type = elem.get('sport')
                break
    return activity_type


def parsing_sports_from_json(directory):
    """Returns a dictionary of activities from folder with json files."""
    sports = {}
    for file_name in os.listdir(directory):
        if not file_name.endswith('.json'):
            continue
        json_file_path = os.path.join(directory, file_name)
        sport = get_json_activity_type(json_file_path)
        if sport not in sports:
            sports[sport] = 0
        sports[sport] += 1
    return sports


if __name__ == '__main__':
    DIRECTORY = os.path.join(os.getcwd(), 'data\\data Ekaterina\\Workouts')
    print(parsing_sports_from_json(DIRECTORY))
