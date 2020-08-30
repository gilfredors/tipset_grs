import os
from online_data.data_fetcher import DataFetcher


def get_football_api():
    with open('.env', 'r') as f:
        api_key = f.read()
        return api_key


def main():
    print("Welcome to GRS's custom football tips predictor")
    log_dir = os.path.join(os.path.dirname(__file__), 'online_data', 'log')
    f = DataFetcher(log_dir, get_football_api())
    data = f.get('countries')
    print('EXIT')


if '__main__' == __name__:
    main()
