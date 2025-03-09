from database import db
from flask_login import UserMixin
from datetime import datetime
import pytz

br_timezone = pytz.timezone("America/Sao_Paulo")

#Function for get datetime the local
def get_brazil_time():
    return datetime.now(br_timezone).replace(tzinfo=None)


class Meal(db.Model,UserMixin):
  #Structure of meal table template 
  id = db.Column(db.Integer, primary_key=True)
  meal = db.Column(db.String, nullable=False)
  description = db.Column(db.String,nullable=False)
  date = db.Column(db.DateTime, default=get_brazil_time) 
  is_on_diet = db.Column(db.Boolean,nullable=False,default=True)

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)