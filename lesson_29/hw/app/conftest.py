import pytest
from db_driver import DatabaseHandler, TestDataset
from logger_conf import logger
from functools import wraps


@pytest.fixture(scope='session')
def db_for_testing():
    """ Creating test database driver. """

    db = DatabaseHandler(TestDataset)
    yield db
    TestDataset.__table__.drop(bind=db.engine, checkfirst=True)
    logger.info("Test table dropped. Database connection closed")


def logger_decorator(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get('request', None)
            test_name = request.node.name
            try:
                result = func(*args, **kwargs)
                logger.info(f"{test_name} - PASSED, {result}")
            except AssertionError as e:
                logger.error(f"{test_name} - FAILED, {str(e).splitlines()[0]}")
                raise
            except Exception as e:
                logger.error(f"{test_name} - ERROR, {str(e).splitlines()[0]}")
                raise
        return wrapper
    return decorator
