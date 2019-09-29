from jsonobject import *


class ErrorResponse(JsonObject):
    general_error = StringProperty
    code = StringProperty
    errors = StringProperty

