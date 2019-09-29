import re
from jsonobject import *


class SignUpBody(JsonObject):
    email = StringProperty
    password = StringProperty
    confirm_password = StringProperty



