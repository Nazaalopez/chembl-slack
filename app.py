#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv
import requests
import json

import bottle
from bottle import Bottle
from bottle import debug, request, route, response, post

from resolver import resolve

app = Bottle()

TOKEN = 'dWwqGfNcPy2gcwZu41zc2BuN'

@app.post('/chem')
def chem():
    # Check the token and make sure the request is from our team
    if hasattr(request, 'forms') and request.forms['token'] == TOKEN:
        text = request.forms['text']
        ret = resolve(text)
        if not ret:
            reply = "Provided identifier couldn't be resolved :("
        elif ret.get(1):
            reply = ret.get(1)
        else:
            "This compound wasn't found in ChEMBL but it can be found in following databases:"
    return reply

debug(True)
app.run(host='0.0.0.0', port=argv[1])
