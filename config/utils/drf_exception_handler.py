import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from requests import ConnectionError

logger = logging.getLogger("api")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, ConnectionError):
        err_data = {
            "success": False,
            "message": "Connection Error",
        }
        logger.error(f"Original error detail and callstack: {exc}")
        return JsonResponse(err_data, safe=False, status=503)
    return response
