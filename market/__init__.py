from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '213cff89e45ae95fc68bf9c8'
db = SQLAlchemy(app) # basically we specify the DB manager SQLAlchemy will work on this particular app scope
bcrypt = Bcrypt(app) # basically we specify the encryption will work on this particular app scope

login_manager = LoginManager(app) # basically we specify the login manager will work on this particular app scope
login_manager.login_view = "login_page" #simply redirects to another page if the user isn't logged in and it visits a forbidden page (made by @login_required decorator 
                                        #in the routes.py file)
login_manager.login_message_category = "info"

from market import routes #we have the market folder, in where we can find the routes "/route"