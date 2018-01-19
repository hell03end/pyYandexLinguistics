import pytest

from pyLinguist import Speller
from pyLinguist.utils.exc import YaTranslateException


class TestSpeller:
    def setup_class(self):
        self.s_json = Speller()
        assert self.s_json
        assert self.s_json.ok

    def test_get_langs(self):
        langs = self.s_json.get_langs()
        assert langs
        assert isinstance(langs, set)

    def test_ok(self):
        assert self.s_json.ok

    def test__check_json(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.s_json._check('', '')
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.s_json._check("text", '', lang=["cpp"])
        suggestion = self.s_json._check("text", "hella")
        assert suggestion
        assert isinstance(suggestion, list)
