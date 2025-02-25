from flask import Flask
from database import db
from model.meals import Meal

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route("/meal",methods=["GET"])
def create_meal():
  return "Hello Porra"

if __name__ == '__main__':
  app.run(debug=True)
