# exception_handlers.py
from rest_framework import status
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as SerializerValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call the default exception handler first, to get the standard error response
    response = exception_handler(exc, context)

    if isinstance(exc, SerializerValidationError) or isinstance(exc, RestValidationError):
        # If the exception is a ValidationError, handle it here
        return Response({"errors": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    return response
