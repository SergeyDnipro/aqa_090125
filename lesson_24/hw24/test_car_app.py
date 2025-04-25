import pytest
import requests
from requests import JSONDecodeError
from car_data import cars_db
from logger_conf import logger
from requests.auth import HTTPBasicAuth


BASE_URL = 'http://127.0.0.1:8080'
USERNAME_DATA = [
    ("", "qwerty"),
    ("User1", ""),
    ("admin", "admin"),
]

QUERY_SEARCH_DATASET = [
    (("price", 2), (cars_db[8], 2)),
    (("price", "n"), (cars_db[8], len(cars_db))),
    (("year", 5), (cars_db[7], 5)),
    (("engine_volume", 3), (cars_db[21], 3)),
    (("brand", 10), (cars_db[16], 10)),
    (("", 100), (cars_db[16], len(cars_db))),
]


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


@pytest.fixture(scope='class', params=USERNAME_DATA)
def username_testcase_data(request):
    return request.param


def validate_json(request, response):
    return response.json()


class TestCarAPI:

    def test_get_all_cars(self, request, set_user_session):
        session = set_user_session
        response = session.get(BASE_URL + '/cars')
        assert response.status_code == 200
        cars = validate_json(request, response)
        logger.info(f"{request.node.name} - PASSED, Get all cars")


    def test_auth_negative(self, request, username_testcase_data):
        user, password = username_testcase_data
        response = requests.post(
            url=BASE_URL + '/auth',
            auth=HTTPBasicAuth(user, password)
        )
        assert response.status_code == 401
        json_data = validate_json(request, response)
        logger.info(f"{request.node.name} - PASSED: {json_data['message']}, QueryParams: user='{user}', password='{password}")


    @pytest.mark.parametrize('query_params, expected_data', QUERY_SEARCH_DATASET)
    def test_car_app_with_query_params(self, query_params, expected_data, set_user_session, request):
        session = set_user_session
        params = {'sort_by': query_params[0], 'limit': query_params[1]}
        try:
            response = session.get(BASE_URL + '/cars', params=params)
            json_data = validate_json(request, response)
            assert response.status_code == 200
            assert len(json_data) == expected_data[1]
            assert json_data[0] == expected_data[0]
            logger.info(f"{request.node.name} - PASSED, QueryParams: sort_by={query_params[0]}, limit={query_params[1]}")
        except Exception as e:
            logger.error(f"{request.node.name} - FAILED: QueryParams: sort_by={query_params[0]}, limit={query_params[1]}, status code={e.args}")
            assert False

    def test_car_app_with_anon_user(self, request):
        response = requests.get(BASE_URL + '/cars')
        logger.info(f"{request.node.name} - PASSED: {response.json()}, {response.status_code}")
