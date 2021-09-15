import functools
from ..config.config import Config

LOGGER = Config().get_logger()


def debug(f: 'function') -> 'function':
    """This function writes to the log the name of the function that is being called when it starts and ends."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        LOGGER.info(f'Calling {f.__name__!r}')
        response = f(*args, **kwargs)
        LOGGER.info(f'Completed {f.__name__!r}')
        return response
    return wrapper
