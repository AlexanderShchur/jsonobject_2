import time
import random
import pytest
import requests
import logging

from models.user_with_session_response import UserWithSessionResponse
from models.error_response import ErrorResponse
from constants import BASE_URL, SUCCESSFULLY_CREATED, HEADERS
from models.sign_up_body import SignUpBody

positive_test_data = [
    {
        'email': f"email{int(time.time())}@example.com",
        'password': 'qwerty1',
        'confirm_password': 'qwerty1'
    },
    {
        'email': f"email{random.randint(10000, 100000)}@example.com",
        'password': 'qwerty1',
        'confirm_password': 'qwerty1'
    }
]

negative_test_data = [
    {
        # email already exists
        'email': 'email@example.com',
        'password': 'qwerty1',
        'confirm_password': 'qwerty1',
        'code': 422,
        'errors': 'user with such email already exist'
    },
    {
        # password should be consists more than 6 symbols
        'email': 'z12345@example.com',
        'password': 'qwerty',
        'confirm_password': 'qwerty',
        'code': 400,
        'errors': {'password': ['Password should have 1 letter and 1 digit. Password cannot contain spaces.']}
    },
    {
        # password and confirm password does not match
        'email': 'z12345@example.com',
        'password': 'qwerty1',
        'confirm_password': 'qwerty12',
        'code': 400,
        'errors': {'confirm_password': ['Passwords do not match.']}
    },
    {
        # password should be contain at least 1 digit
        'email': 'z12345@example.com',
        'password': 'qwertyu',
        'confirm_password': 'qwertyu',
        'code': 400,
        'errors': {'password': ['Password should have 1 letter and 1 digit. Password cannot contain spaces.']}
    }
]

logging.basicConfig(filename="sign_up.log", filemode="w", level=logging.INFO, format='%(asctime)s - %(name)s - %('
                                                                                     'levelname)s - %(''message)s')


@pytest.fixture(params=positive_test_data)
def positive_fixture(request):
    return request.param


@pytest.fixture(params=negative_test_data)
def negative_fixture(request):
    return request.param


def test_sign_up_positive_scenario(positive_fixture):
    user_to_register = SignUpBody(email=positive_fixture['email'], password=positive_fixture['password'],
                                  confirm_password=positive_fixture['confirm_password'])
    r = requests.post(url=f'{BASE_URL}/auth/register', json=user_to_register.to_json(), headers=HEADERS)
    if r.status_code == SUCCESSFULLY_CREATED:
        logging.info(UserWithSessionResponse(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))


def test_sign_up_negative_scenario(negative_fixture):
    user_to_register = SignUpBody(email=negative_fixture['email'], password=negative_fixture['password'],
                                  confirm_password=negative_fixture['confirm_password'])
    expected_code = negative_fixture['code']
    expected_message = negative_fixture['errors']
    r = requests.post(url=f'{BASE_URL}/auth/register', json=user_to_register.to_json(), headers=HEADERS)
    # check code
    assert expected_code == r.status_code
    # check error message
    assert expected_message == r.json()['errors']
    if r.status_code == SUCCESSFULLY_CREATED:
        logging.info(UserWithSessionResponse(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))
