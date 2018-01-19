import os
import pytest

from pyLinguist import Predictor
from pyLinguist.utils.exc import YaTranslateException

try:
    from config import API_KEY_YA_PREDICTOR
except ImportError:
    API_KEY_YA_PREDICTOR = ""


class TestPredictor:
    def setup_class(self):
        self.api_key = os.environ.get(
            "API_KEY_YA_PREDICTOR",
            API_KEY_YA_PREDICTOR
        )
        assert self.api_key
        self.p_json = Predictor(self.api_key)
        assert self.p_json
        assert self.p_json.ok

    def test_get_langs_json(self):
        langs = self.p_json.get_langs()
        assert langs
        assert isinstance(langs, list)

    def test_ok(self):
        assert self.p_json.ok

    def test_complete_json(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.p_json.complete("cpp", "#include")
        prediction = self.p_json.complete('en', "hello", limit=1)
        assert prediction
        assert isinstance(prediction, dict)
        assert 'endOfWord' in prediction
        assert prediction['endOfWord']
        assert 'text' in prediction
        assert len(prediction['text']) == 1
        prediction = self.p_json.complete('en', "hel", limit=5)
        assert prediction
        assert 'endOfWord' in prediction
        assert not prediction['endOfWord']
        assert 'text' in prediction
        assert len(prediction['text']) == 5
