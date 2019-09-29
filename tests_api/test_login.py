import requests
import logging

from models.sign_in_body import *
from models.user_with_session_response import UserWithSessionResponse
from models.error_response import ErrorResponse

from constants import BASE_URL, SUCCESS, HEADERS

logging.basicConfig(filename="login.log", filemode="w", level=logging.INFO, format='%(asctime)s - %(name)s - %('
                                                                                   'levelname)s - %(''message)s')


def test_login_positive_scenario():
    body = {
        'email': "email@example.com",
        'password': 'qwerty1'
    }
    user_to_login = SignInBody(email=body['email'], password=body['password'])
    r = requests.post(url=f'{BASE_URL}/auth/login', json=user_to_login.to_json(), headers=HEADERS)
    if r.status_code == SUCCESS:
        logging.info(UserWithSessionResponse(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))


def test_login_negative_scenario():
    body = {
        'email': "email@example.com",
        'password': 'qwerty1qwe',
        'errors': 'invalid credentials',
        'code': 400
    }
    user_to_login = SignInBody(email=body['email'], password=body['password'])
    expected_message = body['errors']
    r = requests.post(url=f'{BASE_URL}/auth/login', json=user_to_login.to_json(), headers=HEADERS)
    # check error message
    assert expected_message == r.json()['errors']
    if r.status_code == SUCCESS:
        logging.info(UserWithSessionResponse(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))
