import requests
from datetime import datetime as dt
from os.path import exists
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

all_timetables = requests.get("https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable").json()

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

my_info = {
    "INTAKE": "",
    "GROUPING":  "",
}
calendar_id = "",


def main():
    my_timetable = get_timetable(my_info["INTAKE"], my_info["GROUPING"])
    credentials = get_credentials()

    for period in my_timetable:
        start = period["TIME_FROM_ISO"]
        end = period["TIME_TO_ISO"]
        title = period["MODULE_NAME"]
        place = period["ROOM"]
        mod_id = period["MODID"]

        insert_new_event(start, end, title, mod_id, place, credentials)


def get_timetable(intake, grouping):
    my_timetables = []

    for timetable in all_timetables:
        is_my_timetable = intake == timetable["INTAKE"] and grouping == timetable["GROUPING"]
        is_later = dt.today().date() <= dt.strptime(timetable["DATESTAMP_ISO"], '%Y-%m-%d').date()
        if is_my_timetable and is_later:
            my_timetables.append(timetable)

    return my_timetables


def get_credentials():
    credentials = None
    if exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials


def insert_new_event(time_from, time_to, class_title, mod_id, room, credentials):
    service = build("calendar", "v3", credentials=credentials)

    event = {
        'summary': mod_id,
        'location': room,
        'description': class_title,
        'start': {
            'dateTime': time_from,
        },
        'end': {
            'dateTime': time_to,
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    my_info["INTAKE"] = input("Please enter your intake code: ")
    my_info["GROUPING"] = input("Please enter your group number (G1 if none): ")
    calendar_id = input("Please enter your calendar ID: ")
    main()
