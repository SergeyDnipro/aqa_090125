import pytest
import requests
from car_data import cars_db
from logger_conf import logger
from requests.auth import HTTPBasicAuth
from functools import wraps


BASE_URL = 'http://127.0.0.1:8080'
USERNAME_DATA = [
    ("", "qwerty"),
    ("User1", ""),
    ("admin", "admin"),
]

QUERY_SEARCH_DATASET = [
    (("price", 2), (cars_db[8], 2)),
    (("price", ""), (cars_db[8], len(cars_db))),
    (("year", 5), (cars_db[7], 5)),
    (("engine_volume", 3), (cars_db[21], 3)),
    (("brand", 10), (cars_db[16], 10)),
    (("", 100), (cars_db[16], len(cars_db))),
]


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


@pytest.fixture(scope="class")
def set_user_session():
    default_username = "test_user"
    default_password = "test_pass"
    auth_response = requests.post(
        url=BASE_URL + "/auth",
        auth=HTTPBasicAuth(default_username, default_password)
    )
    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {auth_response.json()["access_token"]}'})
    logger.info(f'Test session created for user: {default_username}')
    yield session
    logger.info(f'Test session closed for user: {default_username}')


@pytest.fixture(params=USERNAME_DATA)
def username_testcase_data(request):
    return request.param
