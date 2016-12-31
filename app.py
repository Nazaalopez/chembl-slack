#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import json
import re

from bottle import Bottle
from bottle import debug, request, route, response, post

from resolver import resolve
from chembl_webresource_client.new_client import new_client

app = Bottle()
molecule = new_client.molecule
molecule.set_format('json')

TOKEN = 'dWwqGfNcPy2gcwZu41zc2BuN'
inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')

from compound_view import render_compound

@app.post('/chem')
def chem():
    # Check the token and make sure the request is from our team
    reply = None
    if hasattr(request, 'forms') and request.forms['token'] == TOKEN:
        text = request.forms['text']
        if text.startswith('CHEMBL') or inchi_key_regex.match(text):
            reply = molecule.get(text)   
        else:    
            ret = resolve(text)
            if not ret:
                ret = molecule.search(text)
                if not len(ret):
                    return "Provided identifier couldn't be resolved :white_frowning_face:"
                else:
                    reply = ret[0]
            elif ret.get(1):
                reply = molecule.get(ret.get(1))
        if reply:        
            msg = render_compound(reply)
            chembl_id = reply["molecule_chembl_id"]
            response.content_type = 'application/json'
            return json.dumps(msg)
        else:
            return "This compound wasn't found in ChEMBL but it can be found in following databases:"

debug(True)
app.run(host='0.0.0.0', port=argv[1])
