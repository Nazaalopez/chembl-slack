import json
from resolver import resolve
from chembl_webresource_client.new_client import new_client
from bottle import debug, request, route, response, post

@app.post('/chem')
def chem():
    # Check the token and make sure the request is from our team
    reply = None
    if hasattr(request, 'forms') and request.forms['token'] == config.get('token'):
        text = request.forms['text']  
        ret = resolve(text)
        if not ret:
            return "Provided identifier couldn't be resolved :white_frowning_face:"   
        if isinstance(ret, basestring):
            return ret
        msg = render_compound(ret)
        msg["response_type"] = config.get('response_type', 'ephemeral')
        response.content_type = 'application/json'
    return json.dumps(msg)
