import configparser, os
from typing import List
from flask import jsonify, request, Response
from functools import wraps

def require_auth(f):
    def get_auth_credentials() -> List[str]:
        try:
            directory = os.path.dirname(__file__)
            file = os.path.join(directory, '../../credentials.ini')    
            
            config = configparser.ConfigParser()
            config.read(file)

            return config.get('api-keys', "keys").split(" ")
        except Exception as err:
            return []
        
    keys = get_auth_credentials()

    @wraps(f)
    def authentication_token_check(*args, **kwargs):
        print('Authenticating request')
        try:            
          token = request.headers['Authorization'].split("Bearer ")[1]

          if token in keys:
              return f(*args, **kwargs)
          else:
              message = jsonify(success=False, error=True)
              return message, 401
        except Exception as err:
            print(err)
            message = jsonify(success=False)
            return message, 401

    return authentication_token_check