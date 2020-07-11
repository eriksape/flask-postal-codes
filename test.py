import unittest

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner().run(tests)
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)
