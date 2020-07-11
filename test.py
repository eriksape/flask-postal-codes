import unittest
import flask_testing

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)