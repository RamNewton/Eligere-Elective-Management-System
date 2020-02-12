import unittest
import urllib.request

from flask_testing import LiveServerTestCase
from selenium import webdriver
from config import Config

from app import create_app, db
from app.models import *

test_chair_username = "ram"
test_chair_email = "ram@gmail.com"
test_chair_password = "ram"

test_fac1_fac_id = "FC111"
test_fac1_name = "Vignesh"
test_fac1_designation = "Assistant Professor"
test_fac1_department = "Computer Science"

test_stud1_roll_no = "CSE17354"
test_stud1_name = "Rohit Sai"
test_stud1_batch = "2017-2021"
test_stud1_section = "D"
test_stud1_department = "Computer Science"

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestBase(LiveServerTestCase):
    
    def create_app(self):
        config_name = 'testing'
        app = create_app(TestConfig)
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='sqlite://',
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8943
        )
        return app

    def setUp(self):
        print("hi")
        """Setup the test driver and create test users"""
        dir = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = dir + "\chromedriver.exe"

        self.driver = webdriver.Chrome(executable_path = chrome_driver_path)
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.chair = User(username = test_chair_username, email = test_chair_email)
        self.chair.set_password(test_chair_password)

        self.fac1 = FacultyDetails( fac_id = test_fac1_fac_id,
                                    name = test_fac1_name,
                                    designation = test_fac1_designation,
                                    department = test_fac1_department)

        self.stud1 = StudentDetails(roll_no = test_stud1_roll_no,
                                    name = test_stud1_name,
                                    batch = test_stud1_batch,
                                    section = test_stud1_section,
                                    department = test_stud1_department)

        db.session.add(self.chair)
        db.session.add(self.fac1)
        db.session.add(self.stud1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()