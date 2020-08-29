import os
from online_data.data_fetcher import DataFetcher


def main():
    print("Welcome to GRS's custom football tips predictor")
    log_dir = os.path.join(os.path.dirname(__file__), 'online_data', 'log')
    f = DataFetcher(log_dir)
    data = f.get('countries')
    print('EXIT')


if '__main__' == __name__:
    main()
