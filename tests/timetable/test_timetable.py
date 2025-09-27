from unittest.mock import patch
from datetime import datetime, timedelta

future_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
response = [
    {  # right intake, right group, right time
        "INTAKE": "AFCF2409AS",
        "GROUPING": "G1",
        "MODID": "TEST123",
        "DATESTAMP_ISO": future_date,
        "MODULE_NAME": "Fake Module",
        "DAY": "MON",
        "LOCATION": "APU CAMPUS",
        "ROOM": "S-08-02",
        "LECTID": "MNM",
        "NAME": "Fake Lecturer",
        "SAMACCOUNTNAME": "fakeuser",
        "DATESTAMP": "22-SEP-25",
        "TIME_FROM": "11:45 AM",
        "TIME_TO": "12:45 PM",
        "TIME_FROM_ISO": f"{future_date}T11:45:00+08:00",
        "TIME_TO_ISO": f"{future_date}T12:45:00+08:00",
        "CLASS_CODE": "FAKECODE",
        "COLOR": "yellow",
    },
    {  # right intake, right group, right time, ignored module
        "INTAKE": "AFCF2409AS",
        "GROUPING": "G1",
        "MODID": "IGNOREDMODULE",
        "DATESTAMP_ISO": future_date,
        "MODULE_NAME": "Fake Ignored Module",
        "DAY": "MON",
        "LOCATION": "APU CAMPUS",
        "ROOM": "S-08-02",
        "LECTID": "MNM",
        "NAME": "Fake Lecturer",
        "SAMACCOUNTNAME": "fakeuser",
        "DATESTAMP": "22-SEP-25",
        "TIME_FROM": "11:45 AM",
        "TIME_TO": "12:45 PM",
        "TIME_FROM_ISO": f"{future_date}T11:45:00+08:00",
        "TIME_TO_ISO": f"{future_date}T12:45:00+08:00",
        "CLASS_CODE": "FAKECODE",
        "COLOR": "yellow",
    },
    {  # wrong intake, right group, right time
        "INTAKE": "AWRONGINTAKE",
        "GROUPING": "G1",
        "MODID": "TEST123",
        "DATESTAMP_ISO": future_date,
        "MODULE_NAME": "Fake Module",
        "DAY": "MON",
        "LOCATION": "APU CAMPUS",
        "ROOM": "S-08-02",
        "LECTID": "MNM",
        "NAME": "Fake Lecturer",
        "SAMACCOUNTNAME": "fakeuser",
        "DATESTAMP": "22-SEP-25",
        "TIME_FROM": "11:45 AM",
        "TIME_TO": "12:45 PM",
        "TIME_FROM_ISO": f"{future_date}T11:45:00+08:00",
        "TIME_TO_ISO": f"{future_date}T12:45:00+08:00",
        "CLASS_CODE": "FAKECODE",
        "COLOR": "yellow",
    },
    {  # right everything, but class already passed
        "INTAKE": "AFCF2409AS",
        "MODID": "ABUS011-4-C-OAS-L-3",
        "MODULE_NAME": "Office Administrative Skills",
        "DAY": "MON",
        "LOCATION": "APU CAMPUS",
        "ROOM": "S-08-02",
        "LECTID": "MNM",
        "NAME": "MANOMOHAN A/L A SUPPIAH",
        "SAMACCOUNTNAME": "manomohan",
        "DATESTAMP": "22-SEP-25",
        "DATESTAMP_ISO": "2025-09-22",
        "TIME_FROM": "11:45 AM",
        "TIME_TO": "12:45 PM",
        "TIME_FROM_ISO": "2025-09-22T11:45:00+08:00",
        "TIME_TO_ISO": "2025-09-22T12:45:00+08:00",
        "GROUPING": "G1",
        "CLASS_CODE": "SOF___ABUS011-4-C-OAS-L-3___2025-08-11",
        "COLOR": "yellow",
    },
]


@patch("api.timetable.timetable.requests.get")
def test_right_intake(mock_get):
    mock_get.return_value.json.return_value = response

    from api.timetable.timetable import get_timetable

    x = get_timetable("AFCF2409AS", "G1")
    assert x == response[:2]


@patch("api.timetable.timetable.requests.get")
def test_no_ignored_modules_returned(mock_get):
    mock_get.return_value.json.return_value = response

    from api.timetable.timetable import get_timetable

    x = get_timetable("AFCF2409AS", "G1", ignore_modules=["IGNOREDMODULE"])
    assert x == [response[0]]


@patch("api.timetable.timetable.requests.get")
def test_no_old_classes(mock_get):
    mock_get.return_value.json.return_value = response

    from api.timetable.timetable import get_timetable

    x = get_timetable("AFCF2409AS", "G1", ignore_modules=["IGNOREDMODULE"])
    assert response[-1] not in x
