import json
import logging
import pytest
import requests

from models.error_response import *
from models.user_basic import *
from models.sign_in_body import *
from models.edit_profile_body import *

from constants import SUCCESS, BASE_URL, UNAUTHORIZED, BAD_REQUEST, HEADERS

logging.basicConfig(filename="patch_me.log", filemode="w", level=logging.INFO, format='%(asctime)s - %(name)s - %('
                                                                                      'levelname)s - %(''message)s')


@pytest.fixture(scope='function')
def logged_user():
    body = {
        'email': "email@example.com",
        'password': 'qwerty1'
    }
    user_to_login = SignInBody(email=body['email'], password=body['password'])
    r = requests.post(url=f'{BASE_URL}/auth/login', json=user_to_login.to_json(), headers=HEADERS)
    body = json.loads(r.content)
    token = body['session']['access_token']
    return token


def test_positive_patch_me(logged_user):
    edit_profile = EditProfileBody(first_name="John", last_name="Targarien", bio="The king of all")
    r = requests.patch(url=f'{BASE_URL}/users/me',
                       headers={"Authorization": logged_user},
                       json=edit_profile.to_json())
    if r.status_code == SUCCESS:
        logging.info(UserBasic(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))


def test_negative_patch_me(logged_user):
    edit_profile = EditProfileBody(first_name="John", last_name="Targarien", bio="The king of all")
    r = requests.patch(url=f'{BASE_URL}/users/me',
                       headers={"Authorization": logged_user + '1'},
                       json=edit_profile.to_json())
    assert UNAUTHORIZED == r.status_code or BAD_REQUEST == r.status_code
    if r.status_code == SUCCESS:
        logging.info(UserBasic(r.json()))
    else:
        logging.error(ErrorResponse(r.json()))
