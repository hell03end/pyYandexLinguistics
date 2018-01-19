import logging
import re
from ast import literal_eval
from collections import Generator

from pyLinguist.utils.base import YaBaseAPIHandler
from pyLinguist.utils.log import log


class Translator(YaBaseAPIHandler):
    """
        Implements all Yandex Translator API methods

        for more info look on https://tech.yandex.com/translate/
    """
    _base_url = r"https://translate.yandex.net/api/v{}/tr.json/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'detect': "detect",
        'translate': "translate"
    })

    def __init__(self, api_key: str, version: str='1.5', **kwargs):
        super(Translator, self).__init__(api_key, version, **kwargs)
        self._url = self._base_url.format(self._v)

    @log()
    def get_langs(self, lang: str='en') -> dict:
        """
            Wrapper for getLangs API method.

            Use caching to store received info.
            https://tech.yandex.com/translate/doc/dg/reference/getLangs-docpage
        """
        return super(Translator, self)._get_langs(self._url, ui=lang)

    def getLangs(self, lang: str='en') -> dict:
        return self.get_langs(lang)

    @property
    def directions(self) -> list:
        """ Shortcut for get_langs(...)['dirs'] """
        return self.get_langs().get('dirs', [])

    @property
    def languages(self) -> dict:
        """ Shortcut for get_langs(...)['langs'] """
        return self.get_langs().get('langs', [])

    @property
    def ok(self) -> bool:
        return super(Translator, self)._ok(self._url)

    @log()
    def detect(self,
               text: str,
               hint: list=None,
               post: bool=False,
               **params) -> str:
        """
            Wrapper for detect API method.

            https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/
        """
        if hint and not isinstance(hint, (list, tuple)):
            raise ValueError(
                "'hint' should be iterable, got {}".format(type(hint))
            )

        params = super(Translator, self)._form_params(
            text=text,
            hint=hint,
            **params
        )
        response = super(Translator, self).make_request(
            Translator._make_url(self._url, "detect"), post, **params
        )
        return response['lang']

    @log()
    def translate(self,
                  text: str or list,
                  language: str,
                  formatting: str="plain",
                  options: int=1,
                  post: bool=False,
                  **params) -> dict:
        """
            Wrapper for translate API method.

           https://tech.yandex.com/translate/doc/dg/reference/translate-docpage
        """
        params = super(Translator, self)._form_params(
            text=text,
            list_exceptions={"text"},
            lang=language,
            format=formatting,
            options=options,
            **params
        )
        response = super(Translator, self).make_request(
            Translator._make_url(self._url, "translate"), post, **params
        )

        del response['code']  # this information is redundant
        logging.debug("Remove 'code' key from response.")

        if isinstance(text, list) and len(response['text']) == 1:
            response['text'] = literal_eval(response['text'][0])
        return response

    def translation(self,
                    texts: list or tuple,
                    languages: (list, tuple, str),
                    **params) -> Generator:
        """ Yields translations """
        if not isinstance(texts, (list, tuple)):
            raise ValueError("Expect list|tuple, got '{}'".format(type(texts)))
        if isinstance(languages, str):
            languages = [languages] * len(texts)

        for text, lang in zip(texts, languages):
            yield self.translate(text, lang, **params)
