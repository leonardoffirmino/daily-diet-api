from datetime import datetime
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

#Get all items of user in database
@app.route("/meal",methods=["GET"])
def get_meal():
  user_id = request.args.get("id_user", type=int)

  if not user_id:
    return jsonify({'error':"User not found!"}),404
   
  meals = Meal.query.filter_by(user_id=user_id).all()
    
  meals_list = [meal.to_dict() for meal in meals]

  return jsonify({"Meals": meals_list})

@app.route("/meal/<int:id>", methods=["GET"])
def list_one_meal(id):
  meal = Meal.query.get(id)

  if not meal:
    return jsonify({"Meal not located!"})
  return jsonify({"Meal return": meal.to_dict()})


@app.route("/meal/<int:id>",methods=["PUT"])
def update_meal(id):
  data = request.json
  meal = Meal.query.get(id)

  if not meal:
    return jsonify({'error':'Meal not located!'}),404
  
  try:
    date_str = data.get("date")
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") if date_str else None
  except ValueError:
    return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400

  meal.meal = data.get("meal", meal.meal)
  meal.description = data.get("description", meal.description)
  
  if date_obj:
    meal.date = date_obj
    meal.is_on_diet = data.get("is_on_diet", meal.is_on_diet)

  db.session.commit()

  return jsonify({"message": "Meal updated successfully", "meal": meal.to_dict()})

@app.route("/meal/<int:id>",methods=["DELETE"])
def delete_meal(id):
    meal = db.session.get(Meal, id)  # Usando SQLAlchemy 2.0+

    if not meal:
        return jsonify({"error": "Meal not found!"}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({"message": "Meal deleted successfully"}), 200 

if __name__ == '__main__':
  app.run(debug=True)
