from flask import Flask,jsonify, request
from flask_login import LoginManager

app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/meals', methods=['POST'])
def create_meal():