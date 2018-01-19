""" Base classes """

import json
import logging
from collections import Callable, Iterable
from functools import lru_cache
from http.client import HTTPException
from time import time
from urllib import parse, request

from pyLinguist.utils.exc import YaTranslateException
from pyLinguist.utils.log import log


class YaBaseAPIHandler(object):
    """ Generic class for Yandex APIs """
    _endpoints = {'langs': "getLangs"}

    def __init__(self, key: str, v: str="1", threshold: float or int=86400):
        if not key:
            raise YaTranslateException(401)

        self._v = v
        self._api_key = {
            'key': key,
            'correct': False,
            'timestamp': time() - 60 * 60 * 24,
            'limit': threshold
        }
        logging.debug(
            "set threshold for api key updates to: %d sec.",
            threshold
        )

    @property
    def v(self) -> str:
        """ API version """
        return self._v

    @classmethod
    def _make_url(cls, url: str, endpoint: str) -> str:
        """ Creates full (base url + endpoint) url for API requests """
        return "".join((url, cls._endpoints[endpoint]))

    @log()
    def _form_params(self, list_exceptions: Iterable=(), **params) -> dict:
        """ Prepare params for request """
        for key in params:
            if isinstance(params[key], list) and key not in list_exceptions:
                params[key] = ",".join(params[key])
        parameters = {k: v for k, v in params.items() if v is not None}
        parameters['key'] = self._api_key['key']
        return parameters

    @log()
    @lru_cache(maxsize=4)
    def _get_langs(self, url: str, **params) -> Iterable:
        """ Wrapper for getLangs API method """
        return YaBaseAPIHandler.make_request(
            YaBaseAPIHandler._make_url(url, "langs"),
            post=False,
            **self._form_params(**params)
        )

    @staticmethod
    @log()
    def make_request(url: str,
                     post: bool=False,
                     encoding: str="utf-8",
                     **params) -> dict or list:
        """ Make request to Yandex API """
        url_params = parse.urlencode(params)
        logging.debug("Request '%s' with params '%s'", url, url_params)
        response = None

        if not post:
            full_url = "?".join((url, url_params))
            response = request.urlopen(full_url)
        else:
            response = request.urlopen(url, data=url_params.encode(encoding))

        logging.debug("Response code: %s", response.code)
        if response.code != 200:
            raise YaTranslateException(response.code)

        return json.loads(response.read().decode(encoding))

    @log()
    def _ok(self, url: str=None, func: Callable=None, *args, **params) -> bool:
        """ Is API key correct? """
        if not (self._api_key['correct'] or
                time() - self._api_key['timestamp'] < self._api_key['limit']):
            try:
                if func:
                    __ = func(*args, **params)
                else:
                    __ = self._get_langs(url, **params)
            except (YaTranslateException, HTTPException) as err:
                logging.debug(err)
                self._api_key['correct'] = False
            else:
                self._api_key['timestamp'] = time()
                self._api_key['correct'] = True
        return self._api_key['correct']
