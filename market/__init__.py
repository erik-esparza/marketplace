from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_migrate import Migrate #otherwise, flask db init and flask db migrate won't work
import psycopg2
import os

load_dotenv()

def get_database_uri():
    if 'DB_PASSWORD_FILE' in os.environ:
        with open(os.environ['DB_PASSWORD_FILE']) as f:
            password = f.read().strip()
        return f"postgresql://postgres:{password}@postgres:5432/postgres"
    return os.environ.get('DATABASE_URL', 'sqlite:///market.db')

def get_secret_key():
    if 'SECRET_KEY_FILE' in os.environ:
        with open(os.environ['SECRET_KEY_FILE']) as f:
            return f.read().strip()
    return os.environ.get('SECRET_KEY', 'fallback-dev-key')

def get_resend_key():
    if 'RESEND_KEY_FILE' in os.environ:
        with open(os.environ['RESEND_KEY_FILE']) as f:
            return f.read().strip()
    return os.environ.get('RESEND_KEY', 'fallback-dev-key')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SECRET_KEY'] = get_secret_key()
app.config['RESEND_KEY'] = get_resend_key()
db = SQLAlchemy(app) # basically we specify the DB manager SQLAlchemy will work on this particular app scope

bcrypt = Bcrypt(app) # basically we specify the encryption will work on this particular app scope

login_manager = LoginManager(app) # basically we specify the login manager will work on this particular app scope
login_manager.login_view = "login_page" #simply redirects to another page if the user isn't logged in and it visits a forbidden page (made by @login_required decorator 
                                        #in the routes.py file)
login_manager.login_message_category = "info"

migrate = Migrate(app, db) #init of our migrations superpowers to send this to supabase
from market import routes #we have the market folder, in where we can find the routes "/route"``