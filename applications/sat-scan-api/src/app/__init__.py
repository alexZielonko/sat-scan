from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config_parsers.database_credentials import DatabaseCredentials

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseCredentials().get_db_connection_url()

db = SQLAlchemy(app)

from app.space_objects.routes import space_object_routes

# Register blueprint(s)
app.register_blueprint(space_object_routes)

@app.route('/')
def home():
  return 'Welcome to Sat Scan', 200

@app.route('/health-check')
def health_check():
  return 'Success', 200