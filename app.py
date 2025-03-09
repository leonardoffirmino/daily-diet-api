from model.user import User
from model.meals import Meal
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_required, logout_user,login_user, current_user
from database import db


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
# Session < Conexão ativa do banco de dados
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

  
#View de login para autenticação 
@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    #Login
    user = User.query.filter_by(username=username).first()

    if user:
    # Autenticado com sucesso
      print("Ok")
      return jsonify({"message":"Autenticação realizada com sucesso"})

    return jsonify({"message":"Falha de autenticação!!"})
  
  return jsonify({"message":"Credentials invalid!"}),400

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso"})


#Routes this application
@app.route("/meal",methods=["POST"])
def create_meal():
  data = request.json
  name_meal = data.get("name_meal")
  description_meal = data.get("description_meal")
  is_on_diet = data.get("is_on_diet")

  if name_meal and description_meal:
    new_meal = Meal(meal=name_meal, description=description_meal, is_on_diet=is_on_diet)
    #Insert data the database 
    db.session.add(new_meal)
    db.session.commit()
    return jsonify({'message': "Meal created sucessfully!"})
  
  return jsonify({'message': "Data invalid"})

@app.route("/get_meal",methods=["GET"])
def get_meal():
  return 
  

  

if __name__ == '__main__':
  app.run(debug=True)
