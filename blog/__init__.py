from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "671dc5f30412cbdd1aee12ce7e7989343d04474f7170a2867cb558827be8d4b16ff681d3442d66720a19f52a0e6638dda04eaf44f3fae98dbe20023b19c6b828a2c9f19faef255dee0581310d351d3a3ac6c99c3ef0b84ed006bf8a3dd357d0cfc6330d8f2ae0fa4281e7bd3f910e6c81ede7645c2f6c2c1c53553615e845ae1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


from blog import routes