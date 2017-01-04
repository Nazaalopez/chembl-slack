from bottle import request, response
from chembl_slack import config
import json

class Serialize(object):
    name = 'serialize'
    api = 2

    def apply(self, fn, context):
        def _serialize(*args, **kwargs):
            body = fn(*args, **kwargs)
            if isinstance(body, basestring):
                return body
            elif isinstance(body, dict):
                response.content_type = 'application/json'
                body["response_type"] = config.get('response_type', 'ephemeral')
                return json.dumps(body)
            return None               
        return _serialize
