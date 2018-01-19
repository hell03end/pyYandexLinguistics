import os
import pytest

from pyLinguist import Translator
from pyLinguist.utils.exc import YaTranslateException

try:
    from config import API_KEY_YA_TRANSLATE
except ImportError:
    API_KEY_YA_TRANSLATE = ""


class TestTranslator:
    def setup_class(self):
        self.api_key = os.environ.get(
            "API_KEY_YA_TRANSLATE",
            API_KEY_YA_TRANSLATE
        )
        assert self.api_key
        self.t_json = Translator(self.api_key)
        assert self.t_json
        assert self.t_json.ok

    def test_get_langs_json(self):
        langs = self.t_json.get_langs()
        assert langs
        assert isinstance(langs, dict)
        assert 'dirs' in langs

    def test_directions(self):
        langs = self.t_json.get_langs()
        directions = self.t_json.directions
        assert directions
        assert isinstance(directions, list)
        assert directions == langs['dirs']

    def test_languages(self):
        langs = self.t_json.get_langs()
        languages = self.t_json.languages
        assert langs
        assert isinstance(langs, dict)
        if 'langs' not in langs:
            return
        assert languages
        assert isinstance(languages, dict)
        assert languages == langs['langs']

    def test_ok(self):
        assert self.t_json.ok

    def test_detect_json(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.t_json.detect("hello", hint='en')
        guess_lang = self.t_json.detect("hello")
        assert guess_lang
        assert isinstance(guess_lang, str)
        assert guess_lang == 'en'
        guess_lang = self.t_json.detect("gutten", hint=['de'])
        assert guess_lang
        assert guess_lang == 'de'
        guess_lang = self.t_json.detect("hello", post=True)
        assert guess_lang
        assert guess_lang == 'en'

    def test_translate_json(self):
        translation = self.t_json.translate("hello, world", 'de', options=1)
        assert translation
        assert isinstance(translation, dict)
        assert 'code' not in translation
        assert 'detected' in translation
        translation = self.t_json.translate("hello", 'en-de', options=0)
        assert translation
        assert 'detected' not in translation
        translation = self.t_json.translate(["hello", "world", "cat"], 'de')
        assert translation
        assert 'text' in translation
        assert isinstance(translation['text'], list)
        # assert len(translation['text']) == 3  # until not realized
        translation = self.t_json.translate(['hello, "abs"', 'cat'], 'de')
        assert translation
        assert 'text' in translation
        assert isinstance(translation['text'], list)
        # assert len(translation['text']) == 2)
