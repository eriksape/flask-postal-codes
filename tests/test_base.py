from flask_testing import TestCase
from flask import current_app
from application import application


class MainTest(TestCase):
    def create_app(self):
        application.config['TESTING'] = True
        return application

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_not_found_on_root(self):
        response = self.client.get('/')
        self.assert404(response)
        self.assertEquals(response.json, dict(error='404 Not Found: The requested URL was not found on the server. If '
                                                    'you entered the URL manually please check your spelling and try '
                                                    'again.'))
