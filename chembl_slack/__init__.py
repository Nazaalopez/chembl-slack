
import os
import sys
import bottle
from bottle import Bottle

#-----------------------------------------------------------------------------------------------------------------------

app = Bottle()
config = app.config

#-----------------------------------------------------------------------------------------------------------------------

if not getattr(config, 'load_config'):

        py = sys.version_info
        py3k = py >= (3, 0, 0)

        if py3k:
            from configparser import ConfigParser
        else:
            from ConfigParser import SafeConfigParser as ConfigParser

        from bottle import ConfigDict

        def load_config(self, filename):
            ''' Load values from an *.ini style config file.
                If the config file contains sections, their names are used as
                namespaces for the values within. The two special sections
                ``DEFAULT`` and ``bottle`` refer to the root namespace (no prefix).
            '''
            conf = ConfigParser()
            conf.read(filename)
            for section in conf.sections():
                for key, value in conf.items(section):
                    if section not in ('DEFAULT', 'bottle'):
                        key = section + '.' + key
                    self[key] = value
            return self

        ConfigDict.load_config = load_config

#-----------------------------------------------------------------------------------------------------------------------
