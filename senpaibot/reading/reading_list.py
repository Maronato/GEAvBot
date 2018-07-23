from datetime import datetime
from apiclient.discovery import build
import json
from senpaibot.orderedset import OrderedSet


class BaseReadingList:

    def get_reading_list(self):
        raise NotImplemented

    def get_undated_reading_set(self):
        raise NotImplemented

    @property
    def reading_list(self):
        return self.get_reading_list()

    @property
    def undated_reading_set(self):
        return self.get_undated_reading_set()


class HardcodedReadingList(BaseReadingList):
    """Hardcoded Reading List

    Loads hardcoded data
    """

    _reading_list = [
        ('Capítulo 1', datetime(2018, 5, 22)),
        ('Capítulo 2', datetime(2018, 6, 10)),
        ('Capítulo 3', datetime(2018, 6, 11)),
        ('Capítulo 4', datetime(2018, 6, 12)),
        ('Capítulo 5', datetime(2018, 7, 10)),
        ('Capítulo 6', datetime(2018, 7, 11)),
        ('Capítulo 7', datetime(2018, 7, 12)),
    ]

    def get_reading_list(self):
        return self._reading_list

    def get_undated_reading_set(self):
        return OrderedSet([read[0] for read in self.reading_list])


class JsonReadingList(BaseReadingList):
    """Json Reading List

    Loads json strings in the format:
    [
        ['Cap title', '23/09/18'],
        ['Cap title 2', '05/10/18']
    ]
    """

    datetime_format = '%d/%m/%y'

    def __init__(self, json):
        self.json = json

    def get_json(self):
        return self.json

    def load_json(self):
        return json.loads(self.get_json())

    def date_format_function(self):
        return lambda row: (row[0], datetime.strptime(row[1], self.datetime_format))

    def format_data(self, data):
        return map(self.date_format_function(), data)

    def get_data(self):
        return self.format_data(self.load_json())

    def get_reading_list(self):
        return self.get_data()

    def get_undated_reading_set(self):
        return OrderedSet([read[0] for read in self.reading_list])


class FileReadingList(JsonReadingList):
    """File Reading List

    Loads json files in the format:

    [
        ['Cap title', '23/09/18'],
        ['Cap title 2', '05/10/18']
    ]
    """

    def __init__(self, file):
        self.file = file

    def get_file_path(self):
        return self.file

    def get_file(self):
        return open(self.get_file_path())

    def load_json(self):
        return json.load(self.get_file())


class GoogleSpreadsheetReadingList(JsonReadingList):
    """Google Spreadsheet Reading List

    Loads data from a google spreadsheet in the format:
    Book 1 | Chapter 2 | 14/05/18
    """

    def __init__(self, sheet_id, sheet_range, api_key):
        self.sheet_id = sheet_id
        self.api_key = api_key
        self.sheet_range = sheet_range
        self.data = list(self.get_data())

    def get_service(self):
        return build('sheets', 'v4', developerKey=self.api_key)

    def spreadsheet_format_function(self):
        return lambda row: (', capítulo '.join(row[:2]), datetime.strptime(row[2], self.datetime_format))

    def format_spreadsheet_data(self, data):
        return map(self.spreadsheet_format_function(), data)

    def get_data(self):
        service = self.get_service()
        spreadsheet = service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=self.sheet_range)
        data = spreadsheet.execute().get('values', [])
        return self.format_spreadsheet_data(data)

    def get_reading_list(self):
        return self.data


def get_default_list():
    import os
    sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    api_key = os.environ.get('GOOGLE_API_KEY')
    sheet_range = os.environ.get('GOOGLE_SHEET_RANGE')
    reading_list = GoogleSpreadsheetReadingList(sheet_id, sheet_range, api_key)
    return reading_list
