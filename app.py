#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import json
import time
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

#from chembl_webresource_client.settings import Settings
#Settings.Instance().TOTAL_RETRIES = 1
#Settings.Instance().TIMEOUT = 0.5
#Settings.Instance().NEW_CLIENT_TIMEOUT = 0.5

from compound_template import MESSAGE_TEMPLATE

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
            msg = MESSAGE_TEMPLATE.copy()
            chembl_id = reply["molecule_chembl_id"]
            msg["attachments"][0]["author_name"] = reply["pref_name"]
            msg["attachments"][0]["title"] = chembl_id
            msg["attachments"][0]["title_link"] = "https://chembl-glados.herokuapp.com/compound_report_card/{0}/".format(chembl_id)
            msg["attachments"][0]["image_url"] = "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=500".format(chembl_id)
            msg["attachments"][0]["thumb_url"] = "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=50".format(chembl_id)
            msg["attachments"][0]["text"] = reply["molecule_structures"]["standard_inchi_key"]
            msg["attachments"][0]["fields"][0]["value"] = reply["max_phase"]
            msg["attachments"][0]["fields"][1]["value"] = reply["molecule_properties"]["full_molformula"]
            msg["attachments"][0]["fields"][2]["value"] = reply["molecule_structures"]["canonical_smiles"]
            msg["attachments"][0]["fields"][3]["value"] = reply["molecule_structures"]["standard_inchi"]
            msg["attachments"][0]["ts"] = int(time.time())
            response.content_type = 'application/json'
            return json.dumps(msg)
        else:
            return "This compound wasn't found in ChEMBL but it can be found in following databases:"

debug(True)
app.run(host='0.0.0.0', port=argv[1])
