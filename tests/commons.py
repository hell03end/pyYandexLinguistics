import logging
from collections import Callable


def assert_correct_import(import_func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        exceptions_happend = False
        try:
            import_func(*args, **kwargs)
        except ImportError as err:
            logging.debug(err)
            exceptions_happend = True
        assert not exceptions_happend
    return wrapper
