from flask_testing import TestCase
from app.main import app
import json


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_200_response(self):
        response = self.client.get('/postal-codes')
        self.assert200(response)
        self.assertTrue(isinstance(response.json, list))
        self.assertTrue(response.json is not None)

    def test_check_if_paginate(self):
        pass

    def test_check_adding_limit_paginate_query(self):
        response = self.client.get('/postal-codes?limit=1')
        self.assert200(response)
        self.assertTrue(isinstance(response.json, list))
        self.assertTrue(len(response.json) == 1)
        response = self.client.get('/postal-codes?limit=2')
        self.assert200(response)
        self.assertTrue(isinstance(response.json, list))
        self.assertTrue(len(response.json) == 2)

    def test_check_adding_offset_paginate_query(self):
        response_1 = self.client.get('/postal-codes?limit=1')
        response_2 = self.client.get('/postal-codes?limit=1&offset=1')
        shared_items = {k: response_1.json[k] for k in response_1.json if
                        k in response_2.json and response_1.json[k] == response_2.json[k]}
        self.assertFalse(shared_items)

    def test_check_adding_page_paginate_query(self):
        response_1 = self.client.get('/postal-codes?limit=1')
        response_2 = self.client.get('/postal-codes?limit=1&page=2')
        shared_items = {k: response_1.json[k] for k in response_1.json if
                        k in response_2.json and response_1.json[k] == response_2.json[k]}
        self.assertFalse(shared_items)

    def test_check_offset_is_over_page_paginate_query(self):
        response_1 = self.client.get('/postal-codes?limit=1&offset=20')
        response_2 = self.client.get('/postal-codes?limit=1&page=10')
        response_3 = self.client.get('/postal-codes?limit=1&page=10&offset=20')
        response_4 = self.client.get('/postal-codes?limit=1&page=21')

        response_1 = json.dumps(response_1.json)
        response_2 = json.dumps(response_2.json)
        response_3 = json.dumps(response_3.json)
        response_4 = json.dumps(response_4.json)

        self.assertFalse(response_1 == response_2)
        self.assertTrue(response_1 == response_3)
        self.assertTrue(response_1 == response_4)
        self.assertFalse(response_2 == response_3)
        self.assertFalse(response_2 == response_4)
        self.assertTrue(response_3 == response_4)

    def test_check_sorting_query(self):
        response_1 = self.client.get('/postal-codes?limit=1&sort=codigo_postal')
        response_2 = self.client.get('/postal-codes?limit=1&sort=municipio')
        response_3 = self.client.get('/postal-codes?limit=1&sort=estado')

        response_1 = json.dumps(response_1.json)
        response_2 = json.dumps(response_2.json)
        response_3 = json.dumps(response_3.json)

        self.assertFalse(response_1 == response_2)
        self.assertFalse(response_1 == response_3)
        self.assertFalse(response_2 == response_3)

    def test_check_sorting_order_query(self):
        response_1 = self.client.get('/postal-codes?limit=1&order=ASC')
        response_2 = self.client.get('/postal-codes?limit=1&order=DESC')

        self.assertFalse(json.dumps(response_1.json) == json.dumps(response_2.json))

    def test_add_header_to_response(self):
        response = self.client.get('/postal-codes')
        self.assertTrue(response.headers is not None)
        self.assertTrue('x-total-count' in response.headers)
