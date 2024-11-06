import datetime

import requests

url = "https://school.mos.ru/api/ej/plan/teacher/v1/schedule_items?academic_year_id=12&class_unit_id=943409&from=2024-11-04&to=2024-11-10&with_course_calendar_info=true&with_group_class_subject_info=true&with_lesson_info=true&with_rooms_info=true&page=1&per_page=400&original=true"

headers = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "aid": "12",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyMzQxMjEiLCJzY3AiOiJvcGVuaWQgcHJvZmlsZSIsInN0ZiI6IjMzMzA0NDE3IiwiaXNzIjoiaHR0cHM6XC9cL3NjaG9vbC5tb3MucnUiLCJyb2wiOiIiLCJzc28iOiI4YzIzYWQ3ZS0xNGU0LTQ0YzYtYmVjZC05MmRjYjk4ZjkzNmQiLCJhdWQiOiI5OjkiLCJuYmYiOjE3MzA3ODYzNTgsImF0aCI6InN1ZGlyIiwicmxzIjoiezE5Ols0OTY6MTY6W11dfSx7OTpbNDM6MTpbNTI5XSw1MDo5Ols1MjldLDU0Ojk6WzUyOV0sMTM2OjQ6WzUyOV0sMTgxOjE2Ols1MjldLDE4NDoxNjpbNTI5XSwyMDI6MTc6WzUyOV0sNDAwOjMwOls1MjldLDUyOTo0NDpbNTI5XSw1MzU6NDg6WzUyOV1dfSIsImV4cCI6MTczMTY1MDM1OCwiaWF0IjoxNzMwNzg2MzU4LCJqdGkiOiIxYTU4NTMwZS04MWQ2LTRjMzMtOTg1My0wZTgxZDY0YzMzNmMifQ.mxwsb8_WDp9WZ9zgfaJsxOr9opAIHIPFihKNbw4aC__ikW353bRE_A_qQ91iClotQOVBs0Eu_Qh8sGJveH0ZFjsbrt3ObnjsKejmzyHBh6FUEVDxBIP3nRTqawkB5UMpKaxeC8hr1IrwS9DTVfXmSXfgmWRwlkZDi7AonfPGNep2b7C0glmrpqDVC0AdjtCkBcri0Kjrl-kGET47EfSP3NVBjT_YT7bwKXEzL0klZMh8GbA3TbO6qbCQTH5_88JAwUcDSU9cl2yvWa7jdNK_6QTLtNj4M2Mvz156dr38I70iGy3r0BeQjREtqKqRXInXqfZclO6lHKtnM-8V6GCLCA",
    "priority": "u=1, i",
    "profile-id": "16073051",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-mes-hostid": "9",
    "x-mes-subsystem": "teacherweb"
}

response = requests.get(url, headers=headers)
def get_data():
    # Проверка на статус-код и вывод данных
    if response.status_code == 200:
        data = response.json()
        x = sorted(data, key=lambda item: item['day_number'])
    else:
        print(f"Ошибка {response.status_code}: {response.text}")  # Выводим сообщение об ошибке
        x = []
    return x

def get_dialary(iso_date):
    print(iso_date)
    data = [i for i in get_data() if str(i['iso_date_time']).split('T')[0]==str(iso_date)]

    rasptoday = sorted(data, key=lambda item: item['lesson_number'])
    data_to_send = [{
        'subject_name':i['subject_name'],
        'number':i['lesson_number'],
        'teacher_name':str(i['teacher_name']),
        'room_number': i['room_number'],
        'time': f'{i['time'][0]}:{'00' if i['time'][1]==0 else i['time'][1]}'
    } for i in rasptoday]
    return data_to_send

print(get_dialary(datetime.datetime.now().date()))