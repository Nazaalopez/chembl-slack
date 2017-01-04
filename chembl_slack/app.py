#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import json

from bottle import Bottle
from bottle import debug, request, route, response, post

from bottle import run
from optparse import OptionParser

from resolver import resolve
from chembl_webresource_client.new_client import new_client

from compound_view import render_compound
from chembl_slack import app, config

molecule = new_client.molecule
molecule.set_format('json')

TOKEN = 'dWwqGfNcPy2gcwZu41zc2BuN'

#-----------------------------------------------------------------------------------------------------------------------

parser = OptionParser()
parser.add_option("-c", "--config", dest="config_path",
              help="path to config file", default="slack.conf")

(options, args) = parser.parse_args()
conf_path = options.config_path

config.load_config(conf_path)

#-----------------------------------------------------------------------------------------------------------------------

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
        response.content_type = 'application/json'
        return json.dumps(msg)

def main():
    run(app=app, host=config.get('bottle_host', '0.0.0.0'), port=argv[1],
                                debug=config.get('debug', True), server=config.get('server_middleware', 'tornado'))

if __name__ == "__main__":
    main()
    
