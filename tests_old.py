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
    


if __name__ == '__main__':
    unittest.main(verbosity=2)