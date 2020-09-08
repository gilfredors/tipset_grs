import logging
import os
from online_data.api_get_operations import ApiGetWrapper
from online_data.operations_recorder import OperationsRecorder


def get_football_api_key():
    with open('.env', 'r') as f:
        api_key = f.read()
        return api_key


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    print("Welcome to GRS's custom football tips predictor")
    record_dir = os.path.join(os.path.dirname(__file__), 'online_data', 'log')

    recorder = OperationsRecorder(record_dir)
    api = ApiGetWrapper(recorder, get_football_api_key())
    countries = api.get('countries')
    fixtures_on_date = api.get('fixtures_on_date', formats=['2020-10-03'])
    print('EXIT')


if '__main__' == __name__:
    main()
