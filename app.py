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

  
#Route for create new user in api 
@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  name = data.get("name")

  if username and password:
    #Login
      user = User(username=username,password=password,name=name)
      #Insert data the database 
      db.session.add(user)
      db.session.commit()
      return jsonify({"message":"Autenticação realizada com sucesso"})

    #return jsonify({"message":"Falha de autenticação!!"})
  
  return jsonify({"error":"Credentials invalid!"}),400

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso"})


#Routes this application
@app.route("/meal",methods=["POST"])
def create_meal():
  data = request.json

  # Verifica se user_id foi enviado
  if "user_id" not in data:
    return jsonify({"error": "User ID is required"}), 400

  # Verifica se o usuário existe
  user = User.query.get(data["user_id"])
  if not user:
    return jsonify({"error": "User not found"}), 404
    
 
  name_meal = data.get("name_meal")
  description_meal = data.get("description_meal")
  is_on_diet = data.get("is_on_diet")
  user_id=user.id 

  if name_meal and description_meal:
    new_meal = Meal(meal=name_meal, description=description_meal, is_on_diet=is_on_diet,user_id=user_id)
    #Insert data the database 
    db.session.add(new_meal)
    db.session.commit()
    return jsonify({'message': "Meal created sucessfully!"})
  
  return jsonify({'error': "Data invalid"})

@app.route("/get_meal/<int:id_user>",methods=["GET"])
def get_meal(id_user):
  user_id = User.query.get(id_user)

  if user_id:
    meals = Meal.query.filter_by(user_id=user_id).all()
    
    return jsonify({"Username return --> ":user_id.username},meals)
  
  return jsonify({'error':"User not found!"}),404
  

  

if __name__ == '__main__':
  app.run(debug=True)
