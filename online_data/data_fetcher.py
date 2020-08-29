import json
import logging
import os
import requests
from collections import namedtuple
from datetime import date, datetime


logging.basicConfig(level=logging.DEBUG)


class DataFetcher(object):
    """ DataFetcher class is the interface between program and external API to request data.
    The class keeps a record of all type of records requested in a config file
    """

    Record = namedtuple('Record', ['name', 'date'])
    URL = 'url'
    FREQUENCY = 'update_frequency'
    DEFAULT_FREQUENCY = 0
    REQUEST_FETCHER_LOG = 'request_record.csv'
    REQUEST_DATA_FILE_NAME_FORMAT = '{name}.json'

    GET_CONFIG = {
        'countries': {
            URL: 'https://api-football-v1.p.rapidapi.com/v2/countries',
            FREQUENCY: 1
        }
    }

    def __init__(self, log_dir):
        self.records = []
        self._headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "20f4d7c8b9mshd03c0878beab750p101a30jsn0947b164089d",
        }
        self.log_dir = log_dir
        if os.path.exists(
            os.path.join(
                self.log_dir,
                DataFetcher.REQUEST_FETCHER_LOG)):
            self._read_request_log()

    def get(self, name):
        if name in DataFetcher.GET_CONFIG:
            if self.is_record_updated(name):
                self._update_register()
                data = requests.request(
                    "GET", DataFetcher.GET_CONFIG[name][DataFetcher.URL], headers=self._headers)
                self._store_last_request_in_json(data.json(), name)
                return data.json()
            else:
                return self._read_last_request_in_json(name)
        else:
            logging.error(f'Operation "get {name}" is not supported')

    def is_record_updated(self, name):
        try:
            record = next(x for x in self.records if x.name == name)
            return DataFetcher._update_record_if_time_has_passed(record)
        except StopIteration:
            self.records.append(
                DataFetcher.Record(
                    name=name,
                    date=date.today()))
            return True

    @staticmethod
    def _update_record_if_time_has_passed(record):
        time_has_passed = False
        if (date.today() - record.date).days >= DataFetcher.GET_CONFIG[record.name].get(
                DataFetcher.FREQUENCY, DataFetcher.DEFAULT_FREQUENCY):
            record.date = date.today()
            time_has_passed = True
        return time_has_passed

    def _update_register(self):
        with open(os.path.join(self.log_dir, DataFetcher.REQUEST_FETCHER_LOG), 'w') as log:
            for record in self.records:
                log.write(f'{record.name},{record.date}\n')

    def _store_last_request_in_json(self, data, name):
        with open(os.path.join(self.log_dir, DataFetcher.REQUEST_DATA_FILE_NAME_FORMAT.format(name=name)), 'w') as f:
            json.dump(data, f)

    def _read_last_request_in_json(self, name):
        json_name = os.path.join(
            self.log_dir,
            DataFetcher.REQUEST_DATA_FILE_NAME_FORMAT.format(
                name=name))
        if os.path.exists(json_name):
            with open(json_name, "r") as read_file:
                return json.load(read_file)

    def _read_request_log(self):
        with open(os.path.join(self.log_dir, DataFetcher.REQUEST_FETCHER_LOG), 'r') as log:
            info_lines = log.readlines()
            self.records = list(
                map(DataFetcher._read_record_log_line, info_lines))

    @staticmethod
    def _read_record_log_line(line):
        data = line.replace('\n', '').split(',')
        if len(data) != 2:
            logging.error(f'{line} has not the expected format for record log')
        else:
            return DataFetcher.Record(
                name=data[0], date=datetime.strptime(
                    data[1], '%Y-%m-%d').date())
