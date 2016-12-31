#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv
import requests
import json
import time

import bottle
from bottle import Bottle
from bottle import debug, request, route, response, post
from chembl_webresource_client.new_client import new_client

from resolver import resolve

app = Bottle()
molecule = new_client.molecule
molecule.set_format('json')

TOKEN = 'dWwqGfNcPy2gcwZu41zc2BuN'

MESSAGE_TEMPLATE = {
    "attachments": [
        {
            "fallback": "Compound Report Card",
            "color": "#009688",
            "pretext": "Compound Report Card",
            "author_name": "",
            "title": "",
            "title_link": "https://chembl-glados.herokuapp.com/compound_report_card/{0}/",
            "text": "",
            "fields": [
                {
                    "title": "Max Phase",
                    "value": "",
                    "short": True
                },
                {
                    "title": "Molecular Formula",
                    "value": "",
                    "short": True
                },
                {
                    "title": "Canonical SMILES",
                    "value": "",
                    "short": False
                },
                {
                    "title": "Standard InChI",
                    "value": "",
                    "short": False
                }				
            ],
            "image_url": "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=500",
            "thumb_url": "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=50",
            "footer": "ChEMBL API",
            "footer_icon": "https://avatars0.githubusercontent.com/u/3062531?v=3&s=70",
            "ts": None
        }
    ]
}

@app.post('/chem')
def chem():
    # Check the token and make sure the request is from our team
    if hasattr(request, 'forms') and request.forms['token'] == TOKEN:
        text = request.forms['text']
        ret = resolve(text)
        if not ret:
            return "Provided identifier couldn't be resolved :white_frowning_face:"
        elif ret.get(1):
            reply = molecule.get(ret.get(1))
            msg = MESSAGE_TEMPLATE.copy()
            msg['author_name'] = reply["pref_name"]
            msg['title'] = reply["molecule_chembl_id"]
            msg["title_link"] = msg["title_link"].format(reply["molecule_chembl_id"])
            msg["image_url"] = msg["image_url"].format(reply["molecule_chembl_id"])
            msg["thumb_url"] = msg["thumb_url"].format(reply["molecule_chembl_id"])
            msg["text"] = reply["molecule_structures"]["standard_inchi_key"]
            msg["fields"][0]["value"] = reply["max_phase"]
            msg["fields"][1]["value"] = reply["molecule_properties"]["full_molformula"]
            msg["fields"][2]["value"] = reply["molecule_structures"]["canonical_smiles"]
            msg["fields"][3]["value"] = reply["molecule_structures"]["standard_inchi"]
            msg["ts"] = int(time.time())
            response.content_type = 'application/json'
            return json.dumps(msg)
        else:
            return "This compound wasn't found in ChEMBL but it can be found in following databases:"

debug(True)
app.run(host='0.0.0.0', port=argv[1])
