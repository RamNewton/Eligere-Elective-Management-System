from app import db
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index = True)
    name = db.Column(db.String(40), index=True)
    elective_id = db.Column(db.String(10), index = True)
    def __repr__(self):
        return '<Fac {}, User_id : {}, Elective_id : {}>'.format(self.id, self.user_id, self.elective_id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(40))

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.role)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class InitialElectiveList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    electiveID = db.Column(db.String(64), index = True, unique = True)
    electiveName = db.Column(db.String(64), index=True, unique=True)
    electiveDescription = db.Column(db.String(500))

    def __repr__(self):
        return '<Elective {}>'.format(self.electiveName)

