import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

from app import create_app, db
from app.models import *

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

    def test_AddElectives_fail(self):                                                  #done
        self.login("ram", "ram1")
        self.driver.implicitly_wait(10)

        print("Reached 1")
        a = self.driver.find_element_by_id('Add New')
       # print("Reached 2\n", a)
        a.click()
        self.driver.get('http://localhost:5000/AddElectives')
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

    def test_AddElectives_success(self):                                                       #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram", "ram1")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Add New')
        a.click()
        self.driver.get('http://localhost:5000/AddElectives')

        self.driver.implicitly_wait(10)

        elective_id = self.driver.find_element_by_id("elective_id")
        elective_id.send_keys("CSE888")

        elective_name = self.driver.find_element_by_id("elective_name")
        elective_name.send_keys("Net Centric Programming")

        elective_description = self.driver.find_element_by_id("elective_description")
        elective_description.send_keys("NCP Lab based course")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        # InitialElectiveList.query.filter_by(electiveID = 'CSE888').delete()
        # db.session.commit()
        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Added Elective!")

        self.logout()

    def test_RemoveElectives(self):                                                    #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram", "ram1")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Show List')
        a.click()
        self.driver.get('http://localhost:5000/ShowElectives')
        self.driver.implicitly_wait(10)

        l = self.driver.find_element_by_id('Remove CSE888')
        l.click()
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Access denied")
        self.logout()


    def test_Admin_faculty_success(self):                                            #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("admin", "admin")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Add Faculty')
        a.click()
        self.driver.get('http://localhost:5000/auth/addFacultyDetails')
        self.driver.implicitly_wait(10)

        addfac_id = self.driver.find_element_by_id("fac_id")
        addfac_id.send_keys("FC784")

        addfac_name = self.driver.find_element_by_id("name")
        addfac_name.send_keys("Pradeep")

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

    def test_Regfaculty_fail1(self):                                                    #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Faculty')
            a.click()

            self.driver.get('http://localhost:5000/auth/registerFaculty')
            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC123")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("Pradeep")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("pradeep30@gmail.com")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("Pradeep123")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("Pradeep123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "A user with this Faculty ID already exists")

            self.logout()


    def test_Regfaculty_fail2(self):                                            #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Faculty')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerFaculty')
            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC555")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("Pradeep")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("pradeep30@gmail.com")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("Pradeep123")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("Pradeep123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Faculty ID not found in Database!")

            self.logout()



    def test_Regfaculty_fail3(self):                                                    #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Faculty')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerFaculty')
            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC784")

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
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Username should be between 5 to 16 characters long")

            self.logout()


    def test_Regfaculty_fail4(self):                                                    #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Faculty')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerFaculty')
            self.driver.implicitly_wait(10)

            faculty_id = self.driver.find_element_by_id("fac_id")
            faculty_id.send_keys("FC784")

            faculty_user = self.driver.find_element_by_id("username")
            faculty_user.send_keys("Pradeep")

            faculty_email = self.driver.find_element_by_id("email")
            faculty_email.send_keys("pradeep30@gmail.com")

            faculty_pw = self.driver.find_element_by_id("password")
            faculty_pw.send_keys("Pradeep123")

            faculty_repw = self.driver.find_element_by_id("password2")
            faculty_repw.send_keys("Pardeep123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Field must be equal to password.")

            self.logout()


    def test_Regfaculty_success(self):                                               #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram","ram1")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Register Faculty')
        a.click()
        self.driver.get('http://localhost:5000/auth/registerFaculty')
        self.driver.implicitly_wait(10)

        faculty_id = self.driver.find_element_by_id("fac_id")
        faculty_id.send_keys("FC784")

        faculty_user = self.driver.find_element_by_id("username")
        faculty_user.send_keys("Pradeep")

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
        self.assertEqual(text, "New Faculty User successfully registered!")

        self.logout()



    def test_Admin_student_success(self):                                              #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("admin", "admin")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Add Student')
        a.click()
        self.driver.get('http://localhost:5000/auth/addStudentDetails')
        self.driver.implicitly_wait(10)

        addstu_roll = self.driver.find_element_by_id("roll_no")
        addstu_roll.send_keys("CSE17001")

        addstu_name = self.driver.find_element_by_id("name")
        addstu_name.send_keys("Shreya")


        addstu_depart = self.driver.find_element_by_id("department")
        addstu_depart.send_keys("CSE")

        addstu_sec = self.driver.find_element_by_id("section")
        addstu_sec.send_keys("A")

        addstu_bat = self.driver.find_element_by_id("batch")
        addstu_bat.send_keys("2020")


        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "Student Details Added")

        self.logout()

    def test_Regstudent_fail1(self):                                                  #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Student')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerStudent')
            self.driver.implicitly_wait(10)

            student_roll = self.driver.find_element_by_id("roll_number")
            student_roll.send_keys("CSE17342")

            student_user = self.driver.find_element_by_id("username")
            student_user.send_keys("Shreya")

            student_email = self.driver.find_element_by_id("email")
            student_email.send_keys("shreya@gmail.com")

            student_pw = self.driver.find_element_by_id("password")
            student_pw.send_keys("Shreya123")

            student_repw = self.driver.find_element_by_id("password2")
            student_repw.send_keys("Shreya123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Roll Number not found in Database!")

            self.logout()


    def test_Regstudent_fail2(self):                                              #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Student')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerStudent')
            self.driver.implicitly_wait(10)

            student_roll = self.driver.find_element_by_id("roll_number")
            student_roll.send_keys("CSE17999")

            student_user = self.driver.find_element_by_id("username")
            student_user.send_keys("Shreya")

            student_email = self.driver.find_element_by_id("email")
            student_email.send_keys("shreya@gmail.com")

            student_pw = self.driver.find_element_by_id("password")
            student_pw.send_keys("Shreya123")

            student_repw = self.driver.find_element_by_id("password2")
            student_repw.send_keys("Shreya123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Roll Number not found in Database!")

            self.logout()


    def test_Regstudent_fail3(self):                                              #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Student')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerStudent')
            self.driver.implicitly_wait(10)

            student_roll = self.driver.find_element_by_id("roll_number")
            student_roll.send_keys("CSE17001")

            student_user = self.driver.find_element_by_id("username")
            student_user.send_keys("S")

            student_email = self.driver.find_element_by_id("email")
            student_email.send_keys("shreya@gmail.com")

            student_pw = self.driver.find_element_by_id("password")
            student_pw.send_keys("Shreya123")

            student_repw = self.driver.find_element_by_id("password2")
            student_repw.send_keys("Shreya123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Username should be between 5 to 16 characters long")

            self.logout()

    def test_Regstudent_fail4(self):                                              #done
            self.driver.get("http://localhost:5000/auth/logout")
            self.driver.implicitly_wait(10)
            self.login("ram", "ram1")
            self.driver.implicitly_wait(10)

            a = self.driver.find_element_by_id('Register Student')
            a.click()
            self.driver.get('http://localhost:5000/auth/registerStudent')
            self.driver.implicitly_wait(10)

            student_roll = self.driver.find_element_by_id("roll_number")
            student_roll.send_keys("CSE17001")

            student_user = self.driver.find_element_by_id("username")
            student_user.send_keys("Shreya")

            student_email = self.driver.find_element_by_id("email")
            student_email.send_keys("shreya@gmail.com")

            student_pw = self.driver.find_element_by_id("password")
            student_pw.send_keys("Shreya123")

            student_repw = self.driver.find_element_by_id("password2")
            student_repw.send_keys("Shyrea123")

            submit_button = self.driver.find_element_by_id("submit")
            submit_button.click()

            self.driver.implicitly_wait(10)
            text = self.driver.find_element_by_class_name("help-block").text
            self.assertEqual(text, "Field must be equal to password.")

            self.logout()


    def test_Regstudent_success(self):                                                #done
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("ram", "ram1")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Register Student')
        a.click()
        self.driver.get('http://localhost:5000/auth/registerStudent')
        self.driver.implicitly_wait(10)

        student_roll = self.driver.find_element_by_id("roll_number")
        student_roll.send_keys("CSE17001")

        student_user = self.driver.find_element_by_id("username")
        student_user.send_keys("Shreya")

        student_email = self.driver.find_element_by_id("email")
        student_email.send_keys("shreya@gmail.com")

        student_pw = self.driver.find_element_by_id("password")
        student_pw.send_keys("Shreya123")

        student_repw = self.driver.find_element_by_id("password2")
        student_repw.send_keys("Shreya123")

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        self.driver.implicitly_wait(10)
        text = self.driver.find_element_by_class_name("alert").text
        self.assertEqual(text, "New Student User successfully registered!")

        self.logout()

    def test_Student_Choose(self):
        self.driver.get("http://localhost:5000/auth/logout")
        self.driver.implicitly_wait(10)
        self.login("Shreya", "Shreya123")
        self.driver.implicitly_wait(10)

        a = self.driver.find_element_by_id('Choose Elective Preference')
        a.click()
        self.driver.get('http://localhost:5000/ChooseElectiveToStudy')
        self.driver.implicitly_wait(10)


        l1 = self.driver.find_element_by_id('Pref1 CSE312')
        l1.click()
        self.driver.implicitly_wait(10)
        r1=self.driver.find_element_by_id('Reset First')
        r1.click()
        self.driver.get("http://localhost:5000/funcChooseElectiveToStudy/None/1")

        self.driver.implicitly_wait(10)

        l2 = self.driver.find_element_by_id('Pref2 CSE312')
        l2.click()
        self.driver.implicitly_wait(10)
        r2 = self.driver.find_element_by_id('Reset Second')
        r2.click()
        self.driver.get("http://localhost:5000/funcChooseElectiveToStudy/None/2")

        self.driver.implicitly_wait(10)

        l3 = self.driver.find_element_by_id('Pref3 CSE312')
        l3.click()
        self.driver.implicitly_wait(10)
        r3 = self.driver.find_element_by_id('Reset Third')
        r3.click()
        self.driver.get("http://localhost:5000/funcChooseElectiveToStudy/None/1")


        self.logout()

    @classmethod
    def tearDownClass(inst):
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)