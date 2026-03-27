"""Custom DRF exception handler returning structured JSON errors."""

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response | None:
    response = exception_handler(exc, context)
    if response is None:
        return None

    # Normalise to {"error": "...", "code": "..."}
    if isinstance(response.data, dict):
        # DRF validation errors come as {"field": ["error"]}
        detail = response.data.get("detail")
        if detail:
            response.data = {
                "error": str(detail),
                "code": getattr(exc, "default_code", "error"),
            }
        else:
            # Field-level validation errors — keep them but wrap
            response.data = {
                "error": "Validation failed",
                "code": "validation_error",
                "fields": response.data,
            }
    elif isinstance(response.data, list):
        response.data = {
            "error": response.data[0] if response.data else "Unknown error",
            "code": "error",
        }

    return response
