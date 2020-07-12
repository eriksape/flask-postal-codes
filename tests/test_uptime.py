from flask_testing import TestCase
from flask import current_app

from app.controllers.UptimeController import UptimeController
from app.models import Deployed
from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_check_data_is_saved(self):
        UptimeController.run_sql_script()
        data = current_app.session.query(Deployed).first()
        self.assertTrue(data is not None)
        self.assertTrue(data.ms_time is not None)

    def test_check_uptime_endpoint(self):
        UptimeController.run_sql_script()
        response = self.client.get('/status')
        self.assert200(response)
        self.assertTrue(response.json is not None)

