import json

import pytest
import requests
import logging

from models.error_response import *
from models.sign_in_body import *

from constants import NO_CONTENT, BASE_URL, UNAUTHORIZED, HEADERS

logging.basicConfig(filename="logout.log", filemode="w", level=logging.INFO, format='%(asctime)s - %(name)s - %('
                                                                                    'levelname)s - %(''message)s')


@pytest.fixture(scope='function')
def logged_user():
    body = {
        'email': "email@example.com",
        'password': 'qwerty1'
    }
    user_to_login = SignInBody(email=body['email'], password=body['password'])
    login = requests.post(url=f'{BASE_URL}/auth/login', json=user_to_login.to_json(), headers=HEADERS)
    body = json.loads(login.content)
    token = body['session']['access_token']
    return token


def test_positive_logout(logged_user):
    r = requests.delete(url=f'{BASE_URL}/auth/logout',
                        headers={"Authorization": logged_user})
    assert NO_CONTENT == r.status_code
    if r.status_code == NO_CONTENT:
        logging.info("You are logout")
    else:
        logging.error(ErrorResponse(r.json()))


def test_negative_get_me(logged_user):
    r = requests.delete(url=f'{BASE_URL}/auth/logout',
                        headers={"Authorization": logged_user + '1'})
    assert UNAUTHORIZED == r.status_code
    if r.status_code == NO_CONTENT:
        logging.info("You are logout")
    else:
        logging.error(ErrorResponse(r.json()))
