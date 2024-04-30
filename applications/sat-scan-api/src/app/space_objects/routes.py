from flask import Flask, jsonify, request, Blueprint

from app.space_objects.model import SpaceObject

space_object_routes = Blueprint('space-object', __name__)

@space_object_routes.route('/space-objects', methods=['GET'])
def get_objects():
  return jsonify({"get-all-space-objects": 'success'})

@space_object_routes.route('/space-objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
  return jsonify({ 'get-space-object-endpoint': object_id})