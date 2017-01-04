#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from sys import argv

from bottle import run
from optparse import OptionParser

from chembl_slack import app, config, loadPlugins
from chembl_slack import views

#-----------------------------------------------------------------------------------------------------------------------

parser = OptionParser()
parser.add_option("-c", "--config", dest="config_path",
              help="path to config file", default="chembl_slack/slack.conf")

(options, args) = parser.parse_args()
conf_path = options.config_path

if not os.path.isfile(conf_path):
    raise Exception("file {0} not found...".format(conf_path))

config.load_config(conf_path)
loadApps([])

#-----------------------------------------------------------------------------------------------------------------------

def main():
    run(app=app, host=config.get('bottle_host', '0.0.0.0'), port=argv[1],
                                debug=config.get('debug', True), server=config.get('server_middleware', 'tornado'))

if __name__ == "__main__":
    main()
    
