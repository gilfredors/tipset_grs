import logging
import json
import os
import pandas as pd
from datetime import date, datetime

OPERATION_KEY = 'operation'
DATE_KEY = 'date'


class OperationsRecorder(object):
    """ OperationsRecorder is class that keeps a record of all type of operations requested in a record file to
    external API. It controls also whether new request should be sent to API or data should be fetched from latest
    received data for that operation.
    """

    REQUEST_FETCHER_LOG = 'operations_record.csv'
    REQUEST_DATA_FILE_NAME_FORMAT = '{name}.json'

    def __init__(
            self,
            record_dir,
            record_file_name_with_extension='request_record.csv'):
        self.logger = logging.getLogger('OperationsRecorder')
        self.records = pd.DataFrame(columns=[OPERATION_KEY, DATE_KEY])
        self.record_dir = record_dir
        self.record_file = record_file_name_with_extension
        if os.path.exists(os.path.join(self.record_dir, self.record_file)):
            self._read_request_log()

    def is_operation_run(self, operation, frequency):
        if self.records.empty or self.records[self.records[OPERATION_KEY]
                                              == operation].empty:
            self.records = self.records.append(pd.DataFrame(
                [{OPERATION_KEY: operation, DATE_KEY: date.today()}]), ignore_index=True)
            self.logger.info(
                f'Operation {operation} NOT registered earlier in record')
            return True
        else:
            self.logger.info(
                f'Operation {operation} registered earlier in record. Checking if time has passed since..')
            return self._update_record_if_time_has_passed(operation, frequency)

    def read_last_request(self, name):
        json_name = os.path.join(
            self.record_dir,
            OperationsRecorder.REQUEST_DATA_FILE_NAME_FORMAT.format(name=name))
        with open(json_name, "r") as read_file:
            return json.load(read_file)

    def update_register(self, data, name):
        self.records.to_csv(
            os.path.join(self.record_dir, self.record_file), index=False)
        self._store_data_in_json(data, name)

    def _store_data_in_json(self, data, name):
        with open(os.path.join(self.record_dir, OperationsRecorder.REQUEST_DATA_FILE_NAME_FORMAT.format(name=name)),
                  'w') as f:
            json.dump(data, f)

    def _update_record_if_time_has_passed(self, operation, frequency):
        time_has_passed = False
        record = self.records[self.records[OPERATION_KEY] == operation]
        date_record = datetime.strptime(record.date.iloc[0], "%Y-%m-%d").date()
        if (date.today() - date_record).days >= frequency:
            self.records.loc[self.records[OPERATION_KEY]
                             == operation, DATE_KEY] = date.today()
            time_has_passed = True
            self.logger.info(f'Time has passed.')
        else:
            self.logger.info(f'Time has NOT passed.')
        return time_has_passed

    def _read_request_log(self):
        self.records = pd.read_csv(
            os.path.join(
                self.record_dir,
                self.record_file))
