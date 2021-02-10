def parsing_data_from_csv(row_of_csv, sport_names):
    description = None
    activity_type = row_of_csv['Type']
    if activity_type in sport_names:
        notes = row_of_csv['Notes']
        if notes:
            description = notes
        activity_type = sport_names.get(activity_type)
    else:
        raise ValueError(f'{activity_type} is missing in SPORT_NAMES')

    distance = int(float(row_of_csv['Distance (km)']) * 1000)
    time_string = row_of_csv['Duration']
    elapsed_time = sum(int(t) * 60 ** index for index, t in
                       enumerate(time_string.split(':')[::-1]))
    data = {
        'name': 'Тренировка без GPS',  # required String
        'type': activity_type,  # required String
        'start_date_local': row_of_csv['Date'],  # required Date, ISO 8601
        'elapsed_time': elapsed_time,  # int время в сек
        'distance': distance,  # Float дистанция в метрах
    }
    if description:
        data['description'] = description
    activity_id = row_of_csv['Activity Id']
    parsing_data = {
        'data': data,
        'activity_id': activity_id,
    }
    return parsing_data
