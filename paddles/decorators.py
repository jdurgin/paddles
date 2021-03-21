from functools import wraps
import logging
from pecan.util import _cfg
import sqlalchemy
from paddles.controllers import error
from paddles.models import commit, rollback


log = logging.getLogger(__name__)

def isolation_level(level=None):
    """
    Set an isolation_level for requests using a controller method by applying
    this decorator.

    See http://docs.sqlalchemy.org/en/latest/core/connections.html
    """
    def deco(f):
        _cfg(f)['isolation_level'] = level
        return f
    return deco

def retry_commit(attempts=10):
    """
    Retry a sqlalchemy transaction that fails due to a conflict in the db.
    """
    def deco(f, *args, **kwargs):
        @wraps(f)
        def wrapper(*args, **kwargs):
            log.setLevel(logging.DEBUG)
            log.addHandler(logging.FileHandler('/home/joshd/paddles/extra.log'))
            log.info('decorating...')
            while attempts > 0:
                try:
                    result = f(*args, **kwargs)
                    commit()
                    log.info('success!')
                    return result
                except (sqlalchemy.exc.DBAPIError, sqlalchemy.exc.OperationalError, sqlalchemy.exc.InvalidRequestError):
                    rollback()
                    attempts -= 1
                    if attempts > 0:
                        log.info('retrying transaction due to race')
                    else:
                        log.exception('failed to commit transaction after %d attempts', attempts)
                        error('/errors/unavailable/',
                              'error committing requset. please retry.')
        return wrapper
    return deco
