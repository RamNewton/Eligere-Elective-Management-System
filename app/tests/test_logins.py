import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from app import create_app, db

from app.models import User, InitialElectiveList
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u = User(username = "ram", role = "Chairperson")
        u.set_password("ram")
        db.session.add(u)
        db.session.commit(u)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_chairperson_login(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = dir + "\chromedriver.exe"

        driver = webdriver.Chrome(executable_path = chrome_driver_path)
        driver.implicitly_wait(10)
        driver.maximize_window()

        username_field = driver.find_element_by_id("username")
        username_field.send_keys("vignesh")

        password_field = driver.find_element_by_id("password")
        password_field.send_keys("Vignesh123")

        submit_button = driver.find_element_by_id("submit")
        submit_button.click()

    # def test_password_hashing(self):
    #     u = User(username='susan')
    #     u.set_password('cat')
    #     self.assertFalse(u.check_password('dog'))
    #     self.assertTrue(u.check_password('cat'))

    # def test_elective(self):
    #     el = InitialElectiveList(electiveID = '15CSE444', electiveName = 'What the Heck?', electiveDescription = 'Something')
    #     print(el)
    #     self.assertEqual(el.electiveID, '15CSE444')

if __name__ == '__main__':
    unittest.main(verbosity=2)