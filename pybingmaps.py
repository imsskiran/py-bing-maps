#!/usr/bin/env python

"""
Bing Maps API:  http://www.bingmapsportal.com
Main file for interacting with the Bing Maps API.
"""

from urllib import urlencode
import zlib
import os

try:
    import json
except ImportError:  # pragma: no cover
    # For older versions of Python.
    import simplejson as json

try:
    from urllib2 import urlopen
except ImportError:  # pragma: no cover
    # For Python 3.
    from urllib.request import urlopen


API_KEY = os.environ.get('BING_KEY')


class Bing(object):
    """
    An easy-to-use Python wrapper for the Bing Maps API.
    >>> Bing('my-api-key').search('the lion king')
    Or, if your API key is saved as the `RT_KEY` environment variable,
    the RT class can be initialized like so:
    >>> RT().search('the lion king')
    """

    def __init__(self, api_key='', version=1):
        if not api_key:
            self.api_key = API_KEY
        else:
            self.api_key = api_key
        assert self.api_key is not None, "No API Key"

        if isinstance(version, float):
            version = str(version)  # Eliminate any weird float behavior.
        self.version = version
        BASE_URL = 'http://dev.virtualearth.net/REST/v%s/' % version
        self.BASE_URL = BASE_URL
        self.routes_url = BASE_URL + 'Routes'

    def _load_json_from_url(self, url):
        """
        A wrapper around the api call. The response might be gzipped,
        which this will abstract away. Returns a JSON-decoded dictionary.
        """
        response = urlopen(url).read()

        # the response might be gzip'd
        try:
        # explanation of magic number:
        # http://stackoverflow.com/a/2695466/474683
            response = zlib.decompress(response, 16+zlib.MAX_WBITS)
        except zlib.error:
        # if there's an error, it's probably not gzip'd
            pass
        return json.loads(response)
    def route(self, journeys, **kwargs):
        """
        Bing Maps Route search. Returns a list of dictionaries.
        Kwargs required: wayPoint.1, wayPoint.2
        Possible kwargs include: `wayPoint.2+n', 'heading', 'optimize'
        'avoid', 'distanceBeforeFirstTurn', 'routeAttributes', 'maxSolutions',
        'tolerances', 'distanceUnit', 'mfa'
        """
        search_url = [self.routes_url, '?']
        kwargs.update(journeys)
        kwargs.update({'key': self.api_key})
        search_url.append(urlencode(kwargs))
        data = self._load_json_from_url(''.join(search_url))
        return data
