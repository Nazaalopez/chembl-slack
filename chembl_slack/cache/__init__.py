__author__ = 'mnowotka'

from chembl_slack import config
from chembl_slack.utils import import_class
from chembl_slack.cache.backends.base import BaseCache

cache = None

cache_class = config.get('cache_backend')

if cache_class:
    try:
        cache = import_class(cache_class)()
        if not isinstance(cache, BaseCache):
            print "Configured cache class (%s) is not a BaseCache instance, skipping caching." % cache_class
            cache = None
    except ImportError:
        print 'Error importing %s' % cache_class


