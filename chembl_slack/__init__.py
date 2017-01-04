
import os
import sys
import bottle
from bottle import Bottle
from utils import import_class

#-----------------------------------------------------------------------------------------------------------------------

app = Bottle()
config = app.config

#-----------------------------------------------------------------------------------------------------------------------

DEFAULT_PLUGINS = [
    'chembl_slack.plugins.authorize.Authorize',
    'chembl_slack.plugins.serialize.Serialize',
]

#-----------------------------------------------------------------------------------------------------------------------

def loadPlugins(app, plugins):
    if not plugins:
        plugins = DEFAULT_PLUGINS
    for plugin in plugins:
        try:
            plugin_class = import_class(plugin)
            app.install(plugin_class())
        except Exception as e:
            print "Failed to load plugin %s because of error %s" % (plugin, e.message)
            continue

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
