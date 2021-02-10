import os
from xml.etree import ElementTree


def get_gpx_activity_type(gpx_file_path):
    tree = ElementTree.parse(gpx_file_path)
    root = tree.getroot()
    text = root[0][0].text
    sport_name = text.split(' ')[0]
    return sport_name


def parsing_sports_from_gpx(directory):
    """Returns a dictionary of activities from folder with gpx files."""
    sports = {}
    for file_name in os.listdir(directory):
        if not file_name.endswith('.gpx'):
            continue
        sport = get_gpx_activity_type(os.path.join(directory, file_name))
        if sport not in sports:
            sports[sport] = 0
        sports[sport] += 1
    return sports


def edit_time_in_gpx(directory):
    """Changes the time in the gpx-file."""
    for file_name in os.listdir(directory):
        if not file_name.endswith('.gpx'):
            continue

        gpx_file_path = os.path.join(directory, file_name)
        with open(gpx_file_path, mode='r', encoding='utf-8') as gpx_file:
            data = gpx_file.readlines()

        # меняем время на минус 4 часа
        for i, line in enumerate(data):
            if 'time' not in line:
                continue
            line_split_time = line.split('<time>')
            before_time = line_split_time[0]
            date_time = line_split_time[1].split('</time>')[0]
            after_time = line_split_time[1].split('</time>')[1]

            date_time_split = date_time.split('T')
            hour = date_time_split[1][0:2]
            new_hour = str(int(hour) - 4)
            new_date_time = (date_time_split[0] + 'T' +
                             new_hour + date_time_split[1][2:])

            new_line = (before_time +
                        '<time>' + new_date_time + '</time>' +
                        after_time)
            data[i] = new_line

        # перезаписываем файл
        with open(gpx_file_path, mode='w', encoding='utf-8') as gpx_file:
            gpx_file.writelines(data)


if __name__ == '__main__':
    DIRECTORY = os.path.join(os.getcwd(), 'data')
    print(parsing_sports_from_gpx(DIRECTORY))
