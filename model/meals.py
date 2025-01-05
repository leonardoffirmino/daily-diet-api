from database import db
from flask_login import UserMixin
from datetime import datetime


class Meal(db.Model,UserMixin):
  #Structure of meal table template 
  id = db.Column(db.Integer, primary_key=True)
  meal = db.Column(db.String, nullable=False)
  description = db.Column(db.String,nullable=False)
  date = db.Column(db.Datetime,default=datetime.datetime.utcnow)
  is_on_diet = db.Column(db.Boolean,nullable=False)