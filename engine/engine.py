import logging
from datetime import date
from online_data.transform import transform_fixture_api


class Engine(object):

    def __init__(self, recorder, api, visualizer):
        self.logger = logging.getLogger('Engine')
        self.recorder = recorder
        self.api = api
        self.visualizer = visualizer

    def load_fixture(self, date=date.today()):
        fixture_api = self.api.get('fixtures_on_date', formats=[date])
        leagues_api = self.api.get('leagues')
        fixture = transform_fixture_api(fixture_api, leagues_api)
        return fixture
