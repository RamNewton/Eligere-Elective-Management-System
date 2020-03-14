import unittest
from app import create_app, db
from app.models import *
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_user_row(self):
        u = User(username = "hello", email = "whatever@gmail.com")
        u.set_password('hello')
        db.session.add(u)
        db.session.commit()
        tmp = u.id
        p = User.query.filter_by(id = tmp).first()
        self.assertEqual(p.username, "hello")
        self.assertEqual(p.email, "whatever@gmail.com")
        self.assertTrue(p.check_password('hello'))
        self.assertFalse(p.check_password('hell'))

class FacultyCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_faculty_details(self):
        f = FacultyDetails(fac_id = "CSE333", name = "venkat", designation = "Prof", department = "CSE")
        db.session.add(f)
        db.session.commit()
        p = FacultyDetails.query.filter_by(id = f.id).first()
        self.assertEqual(p.name, "venkat")
        self.assertEqual(p.designation, "Prof")

    def test_add_faculty(self):
        f = FacultyDetails(fac_id = "CSE333", name = "venkat", designation = "Prof", department = "CSE")
        db.session.add(f)
        db.session.commit()

        g = Faculty(fac_id = "CSE333", user_id = f.fac_id, elective_id = "None")
        db.session.add(g)
        db.session.commit()

        querystring = "Select * from faculty, faculty_details where faculty.fac_id = faculty_details.fac_id"
        res = db.engine.execute(querystring)

        for row in res:
            self.assertEqual(row[7], "Prof")
            self.assertEqual(row[6], "venkat")
    

class StudentCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_student_details(self):
        s = StudentDetails(roll_no = "CSE17001", name = "Shreya", batch="2020",section="A", department = "CSE")
        db.session.add(s)
        db.session.commit()
        p = StudentDetails.query.filter_by(id = s.id).first()
        self.assertEqual(p.name, "Shreya")
        self.assertEqual(p.roll_no, "CSE17001")

    def test_add_student(self):
        s = StudentDetails(roll_no = "CSE17001", name = "Shreya", batch="2020",section="A", department = "CSE")
        db.session.add(s)
        db.session.commit()

        g = Student(roll_number = "CSE17001", user_id = s.roll_no,name="Shreya", elective_id1 = "None", elective_id2 = "None", elective_id3 = "None",allocated_elective="None",random_elective="None")
        db.session.add(g)
        db.session.commit()

        querystring = "Select * from student, student_details where student.roll_number = student_details.roll_no"
        res = db.engine.execute(querystring)

        for row in res:
            self.assertEqual(row[3], "CSE17001")
            self.assertEqual(row[11], "Shreya")

class InitialElectiveListCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_initial_elective_list(self):
        i = InitialElectiveList(electiveID = "CSE387",electiveName="OpenLab",electiveDescription="OpenLab Description")
        db.session.add(i)
        db.session.commit()
        p = StudentDetails.query.filter_by(id = i.id).first()
        self.assertEqual(p.electiveID, "CSE387")
        self.assertEqual(p.electiveName, "Open Lab")

    def test_initial_elective_list_check(self):
        f = FacultyDetails(fac_id = "CSE333", name = "venkat", designation = "Prof", department = "CSE")
        db.session.add(f)
        db.session.commit()

        i = InitialElectiveList(electiveID = "CSE387",electiveName="OpenLab",electiveDescription="OpenLab Description")
        db.session.add(i)
        db.session.commit()

        querystring = "Select * from faculty, initial_elective_list where faculty.elective_id = initial_elective_list.electiveID"
        res = db.engine.execute(querystring)

        for row in res:
            self.assertEqual(row[3], "CSE387")
            self.assertEqual(row[6], "Open Lab")

class ElectiveListv2Case(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_elective_listv2(self):
        e = ElectiveListv2(electiveID = "CSE312",electiveName="Pattern Recognition",electiveDescription="Pattern Recognition Details")
        db.session.add(e)
        db.session.commit()
        p = StudentDetails.query.filter_by(id = e.id).first()
        self.assertEqual(p.electiveID, "CSE312")
        self.assertEqual(p.electiveName, "Pattern Recognition")

    def test_elective_listv2_check(self):
        s = StudentDetails(roll_no = "CSE17001", name = "Shreya", batch="2020",section="A", department = "CSE")
        db.session.add(s)
        db.session.commit()

        e = ElectiveListv2(electiveID = "CSE312",electiveName="Pattern Recognition",electiveDescription="Pattern Recognition Details")
        db.session.add(e)
        db.session.commit()

        querystring = "Select * from student, elective_listv2 where student.elective_id1 = elective_listv2.electiveID or student.elective_id2 = elective_listv2.electiveID or student.elective_id3 = elective_listv2.electiveID"
        res = db.engine.execute(querystring)

        for row in res:
            self.assertEqual(row[4], "CSE312")
            self.assertEqual(row[11], "Pattern Recognition")


if __name__ == '__main__':
    unittest.main(verbosity=2)