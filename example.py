import requests
import re
from jsonobject import *


URL = 'http://nls.dev.cleveroad.com/api/Account/Register'
SUCCESS = 200


def validate_email(data):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data):
        raise ValueError(f'Email: {data} is not a valid email!')


class RegisterRequestModel(JsonObject):
    email = StringProperty
    password = StringProperty
    repeat_password = StringProperty(name="repeatPassword")


class BasicResponse(JsonObject):
    ver = StringProperty(name='__v', required=True)


class RegisteredBasic(JsonObject):
    email = StringProperty(required=True, validators=[validate_email])
    email_sent = BooleanProperty(name="emailSent", required=True)


class RegisterResponseModel(BasicResponse):
    data = ObjectProperty(RegisteredBasic)

    def __eq__(self, other):
        return self.data.email == other.email


def sign_up(data):
    print(data.to_json())
    r = requests.post(url=URL, headers={"content-type": "application/json"}, json=data.to_json())
    if r.status_code == SUCCESS:
        return RegisterResponseModel(r.json())
    else:
        return None


user_to_register = RegisterRequestModel(email='ty76lklll5lll@example.com', password='qwerty11',
                                        repeat_password='qwerty11')
result = sign_up(user_to_register)
assert result == user_to_register
