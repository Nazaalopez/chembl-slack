from bottle import request, response
from chembl_slack import config

def authorize(callback):
    def wrapper(*args, **kwargs):
        if hasattr(request, 'forms') and 'token' in request.forms and request.forms['token'] == config.get('token'):
            body = callback(*args, **kwargs)
            return body
        response.status = 401
        return "Not authorized"
    return wrapper
