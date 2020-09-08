import json
import logging
import os
import pandas as pd
import requests
from online_data.api_get_operations import get_frequency, get_url
from datetime import date, datetime


logging.basicConfig(level=logging.DEBUG)


class DataFetcher(object):
    """ DataFetcher class is the interface between program and external API to request data.
    The class keeps a record of all type of records requested in a config file
    """

    REQUEST_FETCHER_LOG = 'request_record.csv'
    REQUEST_DATA_FILE_NAME_FORMAT = '{name}.json'
    OPERATION_KEY = 'operation'
    DATE_KEY = 'date'

    def __init__(self, log_dir, key):
        self.records = pd.DataFrame(
            columns=[
                DataFetcher.OPERATION_KEY,
                DataFetcher.DATE_KEY])
        self._headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': key,
        }
        self.log_dir = log_dir
        if os.path.exists(
            os.path.join(
                self.log_dir,
                DataFetcher.REQUEST_FETCHER_LOG)):
            self._read_request_log()

    def get(self, name, formats=None, params=None):
        if self.is_record_updated(name):
            url_key = get_url(name, formats)
            data = requests.request("GET", url_key, headers=self._headers)
            result_code = data.json().get('api', {}).get('results', 0)
            if result_code != 0:
                self._store_last_request_in_json(data.json(), name)
                self._update_register()
                return data.json()
            else:
                logging.error(
                    f'{data.json().get("message", "Unknown error response from request")}')
        else:
            return self._read_last_request_in_json(name)

    def is_record_updated(self, operation):
        if self.records.empty or self.records[self.records[self.OPERATION_KEY]
                                              == operation].empty:
            self.records = self.records.append(pd.DataFrame(
                [{self.OPERATION_KEY: operation, self.DATE_KEY: date.today()}]), ignore_index=True)
            return True
        else:
            return self._update_record_if_time_has_passed(operation)

    def _update_record_if_time_has_passed(self, name):
        time_has_passed = False
        record = self.records[self.records[self.OPERATION_KEY] == name]
        if (date.today() - record.date[0]
            ).days >= get_frequency(record.operation[0]):
            record.date = date.today()
            time_has_passed = True
        return time_has_passed

    def _update_register(self):
        self.records.to_csv(
            os.path.join(
                self.log_dir,
                DataFetcher.REQUEST_FETCHER_LOG),
            index=False)

    def _store_last_request_in_json(self, data, name):
        with open(os.path.join(self.log_dir, DataFetcher.REQUEST_DATA_FILE_NAME_FORMAT.format(name=name)), 'w') as f:
            json.dump(data, f)

    def _read_last_request_in_json(self, name):
        json_name = os.path.join(
            self.log_dir,
            DataFetcher.REQUEST_DATA_FILE_NAME_FORMAT.format(
                name=name))
        with open(json_name, "r") as read_file:
            return json.load(read_file)

    def _read_request_log(self):
        self.records = pd.read_csv(DataFetcher.REQUEST_FETCHER_LOG, )
