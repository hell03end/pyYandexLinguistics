from functools import lru_cache

from pyLinguist.utils.base import YaBaseAPIHandler
from pyLinguist.utils.exc import YaTranslateException
from pyLinguist.utils.log import log


class Predictor(YaBaseAPIHandler):
    """
        Implements all Yandex Predictor API methods

        for more info look on https://tech.yandex.ru/predictor/
    """
    _base_url = r"https://predictor.yandex.net/api/v{}/predict.json/"
    _endpoints = YaBaseAPIHandler._endpoints.copy()
    _endpoints.update({
        'complete': "complete"
    })

    def __init__(self, api_key: str, version: str='1', **kwargs):
        super(Predictor, self).__init__(key=api_key, v=version, **kwargs)
        self._url = self._base_url.format(self._v)

    def get_langs(self) -> list:
        """
            Wrapper for getLangs API method.
            Use caching to store received info.
            https://tech.yandex.ru/predictor/doc/dg/reference/getLangs-docpage/
        """
        return super(Predictor, self)._get_langs(self._url)

    def getLangs(self) -> list:
        return self.get_langs()

    @property
    def ok(self) -> bool:
        return super(Predictor, self)._ok(self._url)

    @log()
    @lru_cache(maxsize=128)
    def complete(self,
                 lang: str,
                 q: str,
                 limit: int=1,
                 post: bool=False,
                 encoding: str="utf-8") -> dict:
        """
            Wrapper for 'complete' API method.

            https://tech.yandex.ru/predictor/doc/dg/reference/complete-docpage/
        """
        if lang not in self.get_langs():
            raise YaTranslateException(501)

        return super(Predictor, self).make_request(
            Predictor._make_url(self._url, "complete"),
            post=post,
            encoding=encoding,
            **super(Predictor, self)._form_params(
                lang=lang,
                q=q,
                limit=limit
            )
        )
