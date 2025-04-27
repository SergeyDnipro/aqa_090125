import pytest
import requests
from requests import JSONDecodeError
from car_data import cars_db
from logger_conf import logger
from requests.auth import HTTPBasicAuth
from conftest import logger_decorator, BASE_URL, QUERY_SEARCH_DATASET


def validate_json(response):
    try:
        return response.json()
    except JSONDecodeError as e:
        raise AssertionError(e)


class TestCarAPI:
    @logger_decorator(logger)
    def test_get_all_cars(self, request, set_user_session):
        session = set_user_session
        response = session.get(BASE_URL + '/cars')
        assert response.status_code == 200
        json_data = validate_json(response)
        assert len(json_data) == len(cars_db)
        return f"All cars fetched successfully"


    @logger_decorator(logger)
    def test_auth_negative(self, request, username_testcase_data):
        user, password = username_testcase_data

        response = requests.post(
            url=BASE_URL + '/auth',
            auth=HTTPBasicAuth(user, password)
        )

        assert response.status_code == 401
        json_data = validate_json(response)
        return f"{json_data['message']}, QueryParams: user='{user}', password='{password}"


    @logger_decorator(logger)
    @pytest.mark.parametrize('query_params, expected_data', QUERY_SEARCH_DATASET)
    def test_car_app_with_query_params(self, query_params, expected_data, set_user_session, request):
        session = set_user_session
        params = {'sort_by': query_params[0], 'limit': query_params[1]}

        response = session.get(
            url=BASE_URL + '/cars',
            params=params
        )

        assert response.status_code == 200
        json_data = validate_json(response)
        assert len(json_data) == expected_data[1]
        assert json_data[0] == expected_data[0]
        return f"QueryParams: sort_by={query_params[0]}, limit={query_params[1]}"


    @logger_decorator(logger)
    def test_car_app_with_anon_user(self, request):
        response = requests.get(BASE_URL + '/cars')
        assert response.status_code == 401
        json_data = validate_json(response)
        return f"{json_data}"
