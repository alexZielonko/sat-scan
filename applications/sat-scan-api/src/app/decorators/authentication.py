from flask import jsonify, request, Response
from functools import wraps

from app.config_parsers.credentials import Credentials

def require_auth(f):
    api_keys = Credentials().api_keys

    @wraps(f)
    def authentication_token_check(*args, **kwargs):
        print('Authenticating request')
        try:            
          token = request.headers['Authorization'].split("Bearer ")[1]

          print('api_keys')
          print(api_keys)

          if token in api_keys:
              return f(*args, **kwargs)
          else:
              message = jsonify(success=False, error=True)
              return message, 401
        except Exception as err:
            message = jsonify(success=False)
            return message, 401

    return authentication_token_check