from flask_testing import TestCase
from application import application


class MainTest(TestCase):
    def create_app(self):
        application.config['TESTING'] = True
        return application

    def test_getting_a_zip_code(self):
        response = self.client.get('/postal-codes/06060')
        self.assert200(response)
        self.assertTrue('zip_code' in response.json)

    def test_getting_state_data(self):
        response = self.client.get('/postal-codes/06060')
        self.assert200(response)
        self.assertTrue('state' in response.json)
        self.assertTrue('id' in response.json['state'])
        self.assertTrue('name' in response.json['state'])
        self.assertTrue('c_estado' in response.json['state'])

    def test_getting_municipality_data(self):
        response = self.client.get('/postal-codes/06060')
        self.assert200(response)
        self.assertTrue('municipality' in response.json)
        self.assertTrue('id' in response.json['municipality'])
        self.assertTrue('name' in response.json['municipality'])
        self.assertTrue('c_mnpio' in response.json['municipality'])

    def test_getting_settlements_data(self):
        response = self.client.get('/postal-codes/06060')
        self.assert200(response)
        self.assertTrue('settlements' in response.json)
        self.assertTrue(isinstance(response.json['settlements'], list))
        self.assertTrue(response.json['settlements'] is not None)
        self.assertTrue(response.json['settlements'][0] is not None)
        self.assertTrue('name' in response.json['settlements'][0])
        self.assertTrue('type' in response.json['settlements'][0])
        self.assertTrue('id_asenta_cpcons' in response.json['settlements'][0])
        self.assertTrue('c_cve_ciudad' in response.json['settlements'][0])

    def test_validate_postal_code(self):
        response = self.client.get('/postal-codes/6060')
        self.assert400(response)
        self.assertEquals(response.json, dict(message='Not a valid code'))

    def test_not_found_postal_code(self):
        response = self.client.get('/postal-codes/00000')
        self.assert404(response)
        self.assertEquals(response.json, dict(message='Code not found'))
