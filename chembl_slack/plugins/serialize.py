from bottle import request, response
from chembl_slack import config
import json

def authorize(callback):
    def wrapper(*args, **kwargs):
        body = callback(*args, **kwargs)
        if isinstance(body, basestring):
            return body
        elif isinstance(body, dict)::
            response.content_type = 'application/json'
            body["response_type"] = config.get('response_type', 'ephemeral')
            return json.dumps(body)
        return None    
return wrapper
