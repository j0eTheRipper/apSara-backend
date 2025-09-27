import requests
from datetime import datetime as dt


def fetch_tables():
    return requests.get(
        "https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable"
    ).json()


def get_timetable(intake, grouping, ignore_modules=[]):
    all_timetables = fetch_tables()
    my_timetables = []

    for timetable in all_timetables:
        is_my_timetable = (
            intake == timetable["INTAKE"] and grouping == timetable["GROUPING"]
        )
        is_later = (
            dt.today().date()
            <= dt.strptime(timetable["DATESTAMP_ISO"], "%Y-%m-%d").date()
        )
        is_ignored = False
        for mod in ignore_modules:
            if mod in timetable["MODID"]:
                is_ignored = True
                break
        if is_my_timetable and is_later and not is_ignored:
            my_timetables.append(timetable)

    return my_timetables
