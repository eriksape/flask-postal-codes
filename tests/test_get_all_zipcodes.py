from flask_testing import TestCase
from app.main import app


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
        pass

    def test_check_adding_offset_paginate_query(self):
        pass

    def test_check_adding_page_paginate_query(self):
        pass

    def test_check_sorting_query(self):
        pass

    def test_check_sorting_order_query(self):
        pass

    def test_add_header_to_response(self):
        response = self.client.get('/postal-codes')
        self.assertTrue(isinstance(response.headers, list))
        self.assertTrue('x-total-count' in response.headers)
