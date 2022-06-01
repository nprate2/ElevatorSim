import unittest, os, sys

loader = unittest.TestLoader()
start_dir = os.path.join(os.path.dirname(sys.path[0]),'test')
suite = loader.discover(start_dir)
#suite = unittest.TestSuite()
#for all_test_suite in unittest.defaultTestLoader.discover('test', pattern='test_*.py'):
#    for test_suite in all_test_suite:
#        suite.addTests(test_suite)

runner = unittest.TextTestRunner()
runner.run(suite)
