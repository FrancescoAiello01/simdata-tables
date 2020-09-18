from main import app
import unittest


class FlaskTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_calculator(self):
        post_data = {
            'air_pressure': '990',
            'airport_elevation': '1000',
            'outside_air_temp': '35',
            'runway_length_uncorrected': '2750',
            'head_wind': '10',
            'slope_percent': '1',
            'aircraft_weight': '66',
            'ap_registration': 'False',
            'air_conditioning': 'False',
            'engine_anti_ice': 'True',
            'total_anti_ice': 'False',
            'operational_CG_percentage': '26'
            }

        result = self.app.post(
            '/calculate',
            data=post_data
        )
        # check result from server with expected data
        self.assertEqual(
            result.data,
            b'CONFIG 1\nFlex Temp: 51.4\nV1: 135.0\nVR: 136.0\nV2: 140.0'
        )
