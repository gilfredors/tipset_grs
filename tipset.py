import logging
import os
from datetime import datetime
from online_data.api_get_operations import ApiGetWrapper
from online_data.operations_recorder import OperationsRecorder
from engine.engine import Engine


def get_football_api_key():
    with open('.env', 'r') as f:
        api_key = f.read()
        return api_key


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    print("Welcome to GRS's stats and dashboard for matches today")
    record_dir = os.path.join(os.path.dirname(__file__), 'online_data', 'log')

    recorder = OperationsRecorder(record_dir)
    api = ApiGetWrapper(recorder, get_football_api_key())
    visualizer = None
    engine = Engine(recorder, api, visualizer)
    date = '2020-09-19'
    data = engine.load_fixture(date=date)
    print(f'{data.shape[0]} matches for {date}')
    data['time'] = data.apply(lambda x: datetime.fromtimestamp(
        int(x['event_timestamp'])).time(), axis=1)
    print(data.set_index(['country', 'name'])[['homeTeam', 'awayTeam', 'time']].sort_values(
        ['country', 'name', 'time'], ascending=True))


if '__main__' == __name__:
    main()
