#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import json

from bottle import Bottle
from bottle import debug, request, route, response, post

from resolver import resolve
from chembl_webresource_client.new_client import new_client

app = Bottle()
molecule = new_client.molecule
molecule.set_format('json')

TOKEN = 'dWwqGfNcPy2gcwZu41zc2BuN'

from compound_view import render_compound

@app.post('/chem')
def chem():
    # Check the token and make sure the request is from our team
    reply = None
    if hasattr(request, 'forms') and request.forms['token'] == TOKEN:
        text = request.forms['text']  
        ret = resolve(text)
        if not ret:
            return "Provided identifier couldn't be resolved :white_frowning_face:"   
        if isinstance(ret, basestring):
            return ret
        msg = render_compound(ret)
        response.content_type = 'application/json'
        return json.dumps(msg)

debug(True)
app.run(host='0.0.0.0', port=argv[1])
