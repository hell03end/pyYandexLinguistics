import os
import pytest

from pyLinguist import Dictionary
from pyLinguist.utils.exc import YaTranslateException

try:
    from config import API_KEY_YA_DICT
except ImportError:
    API_KEY_YA_DICT = ""


class TestDictionary:
    def setup_class(self):
        self.api_key = os.environ.get("API_KEY_YA_DICT", API_KEY_YA_DICT)
        assert self.api_key
        self.v_json = Dictionary(self.api_key)
        assert self.v_json
        assert self.v_json.ok

    def test_get_langs_json(self):
        langs = self.v_json.get_langs()
        assert langs
        assert isinstance(langs, list)

    def test_ok(self):
        assert self.v_json.ok

    def test_lookup_json(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.v_json.lookup("hello", "cpp")
        definition = self.v_json.lookup("hello", 'en-en')
        assert definition
        assert isinstance(definition, dict)
        assert 'head' not in definition
        assert 'def' in definition

    def test_definitions(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.v_json.definitions("hello", "cpp")
        definition = self.v_json.definitions("hello", 'en-en')
        assert definition
        assert isinstance(definition, list)
