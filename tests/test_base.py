import pytest

from pyLinguist.utils.exc import YaTranslateException
from pyLinguist.utils.base import YaBaseAPIHandler


class TestBaseTypes:
    def setup_class(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = YaBaseAPIHandler(None)
        self.api_key = "123"
        self.h_json = YaBaseAPIHandler(self.api_key)
        assert self.h_json

    def test_attrib_json(self):
        assert self.h_json._api_key
        assert isinstance(self.h_json.v, str)
        self.h_json._v = '1'
        assert self.h_json.v == '1'

    def test__make_url(self):
        base_url = "http://google.com/"
        url = self.h_json._make_url(base_url, "langs")
        assert url
        assert url == base_url + self.h_json._endpoints['langs']
        with pytest.raises(KeyError) as excinfo:
            __ = self.h_json._make_url('', '')
        assert excinfo

    def test__form_params(self):
        params = {
            'a': 1,
            'b': 2
        }
        params_json = self.h_json._form_params(**params)
        assert params_json
        assert isinstance(params_json, dict)
        assert 'key' in params_json
        assert 'a' in params_json
        assert 'b' in params_json
        assert params['a'] == params_json['a']
        assert params['b'] == params_json['b']
