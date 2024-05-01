from flask import Flask, jsonify, request, Blueprint, Response
from marshmallow import ValidationError

from app.space_objects.model import SpaceObject
from app.space_objects.schema import SpaceObjectSchema
from app.decorators.authentication import require_auth

space_object_routes = Blueprint('space-object', __name__)

@space_object_routes.route('/space-objects', methods=['GET'])
def get_objects():
  return jsonify({"get-all-space-objects": 'success'})

@space_object_routes.route('/space-objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
  return jsonify({ 'get-space-object-endpoint': object_id})

@space_object_routes.route('/space-objects', methods=['POST'])
@require_auth
def create_object():
  try:
    valid_object = SpaceObjectSchema().load(request.get_json())
    return jsonify(valid_object), 200
  except ValidationError as err:
    return jsonify(err.messages), 422
  