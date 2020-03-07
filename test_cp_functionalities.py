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
        self.driver.implicitly_wait(10)
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
        self.driver.implicitly_wait(10)
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
        self.driver.implicitly_wait(10)
        a.click()

        self.driver.implicitly_wait(10)

        l = self.driver.find_element_by_id('CSE888 remove')
        l.click()

        self.driver.implicitly_wait(10)

        l = self.driver.find_elements_by_id('CSE888 remove')
        self.assertEqual(l, [])

    # def test_Regfaculty_success(self):
    #     self.driver.get("http://localhost:5000/auth/logout")
    #     self.driver.implicitly_wait(10)
    #     self.login("ram","ram")
    #     self.driver.implicitly_wait(10)

    #     a = self.driver.find_element_by_link_text('Register Faculty')
    #     a.click()

    #     self.driver.implicitly_wait(10)

    #     faculty_id = self.driver.find_element_by_id("fac_id")
    #     faculty_id.send_keys("FC678")

    #     faculty_user = self.driver.find_element_by_id("username")
    #     faculty_user.send_keys("Pradeep")

    #     faculty_email = self.driver.find_element_by_id("email")
    #     faculty_email.send_keys("pradeep30@gmail.com")

    #     faculty_pw = self.driver.find_element_by_id("password")
    #     faculty_pw.send_keys("Pradeep123")

    #     faculty_repw = self.driver.find_element_by_id("password2")
    #     faculty_repw.send_keys("Pradeep123")

    #     submit_button = self.driver.find_element_by_id("submit")
    #     submit_button.click()

    #     self.driver.implicitly_wait(10)
    #     text = self.driver.find_element_by_class_name("alert").text
    #     self.assertEqual(text, "Faculty Registered")

    #     self.logout()

    def test_Regfaculty_fail1(self):
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_link_text('Register Faculty')
            self.driver.implicitly_wait(10)
            a.click()

            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("123")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("Dummy")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("Dummy")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("abc")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("dummy")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Faculty ID not found in Database!")

            self.logout()

    def test_Regfaculty_fail2(self):
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_link_text('Register Faculty')
            self.driver.implicitly_wait(10)
            a.click()

            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC678")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("P")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("pradeep30@gmail.com")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("Pradeep123")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("Pradeep123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("alert").text
            self.assertEqual(text, "Username should be 5 to 16 characters long")

            self.logout()

    def test_Regfaculty_fail3(self):
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_link_text('Register Faculty')
            self.driver.implicitly_wait(10)
            a.click()

            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC678")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("Pradeep")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("pradeep30@gmail.com")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("Pradeep123")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("Parvathi123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("alert").text
            self.assertEqual(text, "Field must be equal password")

            self.logout()

            
    # def test_Regstudent_success(self):
    #     self.driver.get("http://localhost:5000/auth/logout")
    #     self.driver.implicitly_wait(10)
    #     self.login("ram", "ram")
    #     self.driver.implicitly_wait(10)

    #     a = self.driver.find_element_by_link_text('Register Student')
    #     a.click()

    #     self.driver.implicitly_wait(10)

    #     student_roll = self.driver.find_element_by_id("roll_number")
    #     student_roll.send_keys("CB.EN.U4CSE17342")

    #     student_user = self.driver.find_element_by_id("username")
    #     student_user.send_keys("parvathi")

    #     student_email = self.driver.find_element_by_id("email")
    #     student_email.send_keys("parvathi@gmail.com")

    #     student_pw = self.driver.find_element_by_id("password")
    #     student_pw.send_keys("Parvathi123")

    #     student_repw = self.driver.find_element_by_id("password2")
    #     student_repw.send_keys("Parvathi123")

    #     submit_button = self.driver.find_element_by_id("submit")
    #     submit_button.click()

    #     self.driver.implicitly_wait(10)
    #     text = self.driver.find_element_by_class_name("alert").text
    #     self.assertEqual(text, "Student Registered")

    #     self.logout()

    def test_Regstudent_fail(self):
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_link_text('Register Student')
            self.driver.implicitly_wait(10)
            a.click()

            self.driver.implicitly_wait(10)
            student_roll = self.driver.find_element_by_id("roll_number")
            student_roll.send_keys("17342")

            student_user = self.driver.find_element_by_id("username")
            student_user.send_keys("Dummy")

            student_email = self.driver.find_element_by_id("email")
            student_email.send_keys("dummy@gmail.com")

            student_pw = self.driver.find_element_by_id("password")
            student_pw.send_keys("dmmy123")

            student_repw = self.driver.find_element_by_id("password2")
            student_repw.send_keys("dmmy123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Roll Number not found in Database!")

            self.logout()

    def test_Admin_faculty_success(self):  #doubtful
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("admin", "admin")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Add Faculty Details')
        self.driver.implicitly_wait(10)
        a.click()

        self.driver.implicitly_wait(10)

        addfac_id = self.driver.find_element_by_id("fac_id")
        addfac_id.send_keys("FC784")

        addfac_name = self.driver.find_element_by_id("name")
        addfac_name.send_keys("Parthiv")

        addfac_desig = self.driver.find_element_by_id("designation")
        addfac_desig.send_keys("Faculty")

        addfac_depart = self.driver.find_element_by_id("department")
        addfac_depart.send_keys("CSE")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()


        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Faculty Details Added")

        self.logout()

    def test_Admin_faculty_fail1(self):  #doubtful
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("admin", "admin")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Add Faculty Details')
        self.driver.implicitly_wait(10)
        a.click()

        self.driver.implicitly_wait(10)

        addfac_id = self.driver.find_element_by_id("fac_id")
        addfac_id.send_keys("1234")

        addfac_name = self.driver.find_element_by_id("name")
        addfac_name.send_keys("Abinav")

        addfac_desig = self.driver.find_element_by_id("designation")
        addfac_desig.send_keys("Faculty")

        addfac_depart = self.driver.find_element_by_id("department")
        addfac_depart.send_keys("ECE")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("help-block").text
        self.assertEqual(text, "Faculty ID is in unexpected form. Should be like FCXXX")

        self.logout()

    def test_Student_p1(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("rohitsai", "Rohitsai123")
        self.driver.implicitly_wait(10)

        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_link_text('Enter Elective Preference')
        self.driver.implicitly_wait(10)
        a.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Access denied")

        self.logout()

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)