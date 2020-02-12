import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class ChairpersonFunctionalitiesCase(unittest.TestCase):
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

    def test_AddElectives_fail(self):
        self.login("ram", "ram")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Add Electives')
        a.click()

        self.driver.implicitly_wait(10)
        elective_id = self.driver.find_element_by_id("elective_id")
        elective_id.send_keys("CS")

        elective_name = self.driver.find_element_by_id("elective_name")
        elective_name.send_keys("Dummy")

        elective_description = self.driver.find_element_by_id("elective_description")
        elective_description.send_keys("Dummy Desc")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("help-block").text
        self.assertEqual(text, "Elective ID is in unexpected form. Should be like CSEXXX")

        self.driver.implicitly_wait(10)
        self.logout()

    def test_AddElectives_success(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram", "ram")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Add Electives')
        a.click()

        self.driver.implicitly_wait(10)

        elective_id = self.driver.find_element_by_id("elective_id")
        elective_id.send_keys("CSE888")

        elective_name = self.driver.find_element_by_id("elective_name")
        elective_name.send_keys("Net Centric Programming")

        elective_description = self.driver.find_element_by_id("elective_description")
        elective_description.send_keys("NCP Lab based course")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Added Elective!")

        self.logout()
    
    def test_RemoveElectives(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram", "ram")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Show Electives')
        a.click()

        self.driver.implicitly_wait(10)

        l = self.driver.find_element_by_id('CSE888 remove')
        l.click()

        self.driver.implicitly_wait(10)

        l = self.driver.find_elements_by_id('CSE888 remove')
        self.assertEqual(l, [])

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)