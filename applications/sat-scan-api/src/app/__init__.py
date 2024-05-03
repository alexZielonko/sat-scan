from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
# app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@database/development'

# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)

# from app.space_objects.routes import space_object_routes

# # Register blueprint(s)
# app.register_blueprint(space_object_routes)

@app.route('/health-check')
def health_check():
  return 'Success', 200