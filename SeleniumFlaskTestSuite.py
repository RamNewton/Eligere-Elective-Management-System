import unittest
import os
from test_logins import LoginCase
from test_cp_functionalities import ChairpersonFunctionalitiesCase
from HtmlTestRunner import HTMLTestRunner

# get the directory path to output report file
dir = os.getcwd()

login_t = unittest.TestLoader().loadTestsFromTestCase(LoginCase)
cp_t = unittest.TestLoader().loadTestsFromTestCase(ChairpersonFunctionalitiesCase)

test_suite = unittest.TestSuite([login_t, cp_t])

# unittest.TextTestRunner(verbosity=2).run(test_suite)

runner = HTMLTestRunner(output='ui_reports')
runner.run(test_suite)