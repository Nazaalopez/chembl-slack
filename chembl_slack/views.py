from model import resolve
from controller import render_entity
from bottle import request
from chembl_slack import app

@app.post('/chem')
def chem():
    text = request.forms['text']  
    ret = resolve(text)
    if not ret:
        return "Provided identifier couldn't be resolved :white_frowning_face:"
    if isinstance(ret, basestring):
        return ret
    entity_type, entity_id = ret
    msg = render_entity(entity_type, entity_id)
    return msg
