from app import db, models
from app.models import *

u = User(username = 'ram', email = 'ramnewton.a@gmail.com', role = 'Chairperson')
u.set_password('ram')
k = User(username = 'admin', email = 'admin@gmail.com', role = 'Admin')
k.set_password('admin')

db.session.add(u)
db.session.add(k)

db.session.commit()