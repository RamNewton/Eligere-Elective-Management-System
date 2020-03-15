import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class LoginCase(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        dir = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = dir + "\chromedriver.exe"
        inst.driver = webdriver.Chrome(executable_path = chrome_driver_path)
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()

    def login(self, uname, pwd):
        self.driver.get("http://localhost:5000/auth/login")

        username_field = self.driver.find_element_by_id("username")
        username_field.send_keys(uname)

        password_field = self.driver.find_element_by_id("password")
        password_field.send_keys(pwd)

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

    def logout(self):
        link = self.driver.find_element_by_id("logout")
        link.click()

    def test_chairperson_login(self):
        self.login("ram", "ram1")
        text = self.driver.find_element_by_id("greeting").text
        self.assertEqual(text, "Hello, ram!")
        self.logout()

    def test_faculty_login(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("venkat", "Venkat123")
        text = self.driver.find_element_by_id("greeting").text
        self.assertEqual(text, "Hello, venkat!")
        self.driver.implicitly_wait(10)
        self.logout()

    def test_student_login(self):
        self.login("sanjay", "Sanjay123")
        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_id("greeting").text
        self.assertEqual(text, "Hello, sanjay!")
        self.driver.implicitly_wait(10)
        self.logout()


    def test_invalid_login(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("dummy", "dummy")
        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Invalid username or password")

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)