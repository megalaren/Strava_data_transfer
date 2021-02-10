import os
from xml.etree import ElementTree


def get_tcx_activity_type(tcx_file_path):
    tree = ElementTree.parse(tcx_file_path)
    root = tree.getroot()
    sport_name = root[0][0].attrib.get('Sport')
    return sport_name


def parsing_sports_from_tcx(directory):
    """Returns a dictionary of activities from folder with tcx files."""
    sports = {}
    for file_name in os.listdir(directory):
        if not file_name.endswith('.tcx'):
            continue
        sport = get_tcx_activity_type(os.path.join(directory, file_name))
        if sport not in sports:
            sports[sport] = 0
        sports[sport] += 1
    return sports


if __name__ == '__main__':
    DIRECTORY = os.path.join(os.getcwd(), 'data\\data Ekaterina\\Workouts')
    print(parsing_sports_from_tcx(DIRECTORY))
