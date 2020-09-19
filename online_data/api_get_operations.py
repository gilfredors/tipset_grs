import logging
import requests


URL = 'url'
FREQUENCY = 'update_frequency'
DEFAULT_FREQUENCY = 0
REQUEST_FETCHER_LOG = 'request_record.csv'
REQUEST_DATA_FILE_NAME_FORMAT = '{name}.json'

operations = {
    'countries': {
        URL: 'https://api-football-v1.p.rapidapi.com/v2/countries',
        FREQUENCY: 7
    },
    'leagues': {
        URL: 'https://api-football-v1.p.rapidapi.com/v2/leagues',
        FREQUENCY: 7
    },
    'fixtures_on_date': {
        URL: "https://api-football-v1.p.rapidapi.com/fixtures/date/{}",
        FREQUENCY: 1
    }
}


class ApiGetWrapper(object):

    def __init__(self, recorder, key):
        self.logger = logging.getLogger('ApiGetWrapper')
        self.recorder = recorder
        self._headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': key,
        }

    def get(self, operation, formats=None, params=None):
        if operation in operations:
            url = get_url(operation, formats)
            frequency = get_frequency(operation)
            if self.recorder.is_operation_run(url, frequency):
                data = self._request(url)
                if data is not None:
                    self.recorder.update_register(
                        data, self.transform_url_to_name(url))
            else:
                data = self.recorder.read_last_request(
                    self.transform_url_to_name(url))
            return data
        else:
            self.logger.error(f'Operation {operation} is not supported')

    def _request(self, url):
        data = requests.request("GET", url, headers=self._headers)
        result_code = data.json().get('api', {}).get('results', 0)
        if result_code != 0:
            return data.json()
        else:
            self.logger.error(
                f'{data.json().get("message", "Unknown error response from request")}')

    def transform_url_to_name(self, url):
        url_after_host = url.split(self._headers['x-rapidapi-host'][-4:])[1]
        url_after_host_no_characters = url_after_host.replace('/', '')
        return url_after_host_no_characters


def get_url(operation, formats):
    if operation in operations:
        return operations.get(operation).get(URL) if formats is None else \
            operations.get(operation).get(URL).format(*formats)
    else:
        logging.error(f'Operation "get {operation}" is not supported')


def get_frequency(operation):
    if operation in operations:
        return operations.get(operation).get(FREQUENCY, DEFAULT_FREQUENCY)
    else:
        logging.error(f'Operation "get {operation}" is not supported')
