from app import db
from flask import Flask, jsonify, request, Blueprint, Response, abort
from sqlalchemy import exc
from marshmallow import ValidationError

from app.space_objects.model import SpaceObject
from app.space_objects.schema import SpaceObjectSchema
from app.decorators.authentication import require_auth

space_object_routes = Blueprint("space-object", __name__)


@space_object_routes.route("/space-objects", methods=["GET"])
def get_objects():
    try:
        raw_results = SpaceObject.query.all()
        return list(map(lambda res: SpaceObjectSchema().dump(res), raw_results))
    except Exception:
        return {}, 500


@space_object_routes.route("/space-objects/<string:object_id>", methods=["GET"])
def get_object(object_id):
    try:
        result = SpaceObject.query.get(object_id)

        if result:
            return SpaceObjectSchema().dump(result)
        else:
            return {}, 404
    except Exception:
        return {}, 500


@space_object_routes.route("/space-objects/<string:object_id>", methods=["DELETE"])
@require_auth
def delete_object(object_id):
    try:
        result = SpaceObject.query.filter_by(sat_id=object_id).delete()
        db.session.commit()

        if result:
            return {}, 200
        else:
            return {}, 404
    except Exception:
        return {}, 500


@space_object_routes.route("/space-objects", methods=["POST"])
@require_auth
def create_object():
    try:
        valid_object = SpaceObjectSchema().load(request.get_json())
        space_object = SpaceObject(**valid_object)

        db.session.add(space_object)
        db.session.commit()
        return jsonify(valid_object), 200
    except ValidationError as err:
        return jsonify(err.messages), 422
    except exc.IntegrityError:
        return "Record already exists for satellite id", 409
    except Exception as err:
        print(err)
        return "Something went wrong", 500


@space_object_routes.route("/space-objects", methods=["PUT"])
@require_auth
def update_object():
    try:
        valid_object = SpaceObjectSchema().load(request.get_json())

        result = SpaceObject.query.get(valid_object["sat_id"])

        if result == None:
            abort(404)

        if result:
            SpaceObject.query.filter_by(sat_id=valid_object["sat_id"]).delete()
            space_object = SpaceObject(**valid_object)
            db.session.add(space_object)
            db.session.commit()

        return jsonify(valid_object), 200
    except ValidationError as err:
        return jsonify(err.messages), 422
    except Exception as err:
        status_code = err.code if hasattr(err, "code") else 500
        return err, status_code
