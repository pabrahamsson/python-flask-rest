from wsgi import application as app
import json
import unittest

class AppTestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_environment_data(self):
        result = self.app.get('/environment')
        self.assertFalse(json.loads(result.data)['config']['JSONIFY_PRETTYPRINT_REGULAR'])

    def test_environment_status_code(self):
        result = self.app.get('/environment')
        self.assertEqual(result.status_code, 200)

    def test_greeting_data(self):
        result = self.app.get('/greeting')
        self.assertEqual(json.loads(result.data)['content'], 'Hello, World!')

    def test_greeting_data_name(self):
        result = self.app.get('/greeting?name=OpenShift')
        self.assertEqual(json.loads(result.data)['content'], 'Hello, OpenShift!')

    def test_greeting_status_code(self):
        result = self.app.get('/greeting')
        self.assertEqual(result.status_code, 200)

    def test_health_data(self):
        result = self.app.get('/health')
        self.assertEqual(json.loads(result.data)['status'], 'success')

    def test_health_status_code(self):
        result = self.app.get('/health')
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        result = self.app.get('/')
        self.assertEqual(json.loads(result.data)['message'], 'This is my webservice!')
        self.assertEqual(json.loads(result.data)['paths'], "['/', '/greeting', '/hostinfo']")

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_hostinfo_status_code(self):
        result = self.app.get('/hostinfo')
        self.assertEqual(result.status_code, 200)

    def test_hostinfo_data(self):
        result = self.app.get('/hostinfo')
        self.assertIn('hostname', json.loads(result.data))

if __name__ == '__main__':
    unittest.main()
