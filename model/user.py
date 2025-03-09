from database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
  #Table for create a new user in application
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(80),nullable=False, default='user')

    meals = db.relationship("Meal", backref="user", lazy=True)

    
    