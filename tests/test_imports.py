from pyLinguist import *  # to test absolute import
from tests.commons import assert_correct_import


class TestImports:
    def test_import_all(self):
        assert "Translator" in globals()
        assert "Dictionary" in globals()
        assert "Predictor" in globals()
        assert "Speller" in globals()
        assert "YaTranslateException" not in globals()
        assert "_YaAPIHandler" not in globals()

    @assert_correct_import
    def test_direct_import(self):
        import pyLinguist
        assert pyLinguist
        assert "pyLinguist" in locals()
        del pyLinguist

    @assert_correct_import
    def test_from_init(self):
        from pyLinguist import Translator as Tr
        assert Tr
        assert "Tr" in locals()
        del Tr

        from pyLinguist import Dictionary as Dct
        assert Dct
        assert "Dct" in locals()
        del Dct

        from pyLinguist import Predictor as Pr
        assert Pr
        assert "Pr" in locals()
        del Pr

        from pyLinguist import Speller as Sp
        assert Sp
        assert "Sp" in locals()
        del Sp

        from pyLinguist.utils.exc import YaTranslateException as YaT
        assert YaT
        assert "YaT" in locals()
        del YaT

    @assert_correct_import
    def test_from_modules(self):
        from pyLinguist import Translate
        assert Translate
        assert "Translate" in locals()
        assert Translate.Translator
        del Translate

        from pyLinguist import Vocabulary
        assert Vocabulary
        assert "Vocabulary" in locals()
        assert Vocabulary.Dictionary
        assert Vocabulary.Speller
        del Vocabulary

        from pyLinguist import Prediction
        assert Prediction
        assert "Prediction" in locals()
        assert Prediction.Predictor
        del Prediction
