import unittest
import HTMLTestRunner
import os
from test_logins import LoginCase
from test_cp_functionalities import ChairpersonFunctionalitiesCase

# get the directory path to output report file
dir = os.getcwd()

login_t = unittest.TestLoader().loadTestsFromTestCase(LoginCase)
cp_t = unittest.TestLoader().loadTestsFromTestCase(ChairpersonFunctionalitiesCase)

test_suite = unittest.TestSuite([login_t, cp_t])

unittest.TextTestRunner(verbosity=2).run(test_suite)

# outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")

# # configure HTMLTestRunner options
# runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')

# # run the suite using HTMLTestRunner
# runner.run(test_suite)