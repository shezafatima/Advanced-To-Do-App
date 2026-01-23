from typing import Any, Dict
from fastapi import Response
from fastapi.responses import JSONResponse


def create_success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> JSONResponse:
    """
    Create a standardized success response.
    """
    response_data = {
        "success": True,
        "message": message,
        "data": data
    }
    return JSONResponse(content=response_data, status_code=status_code)


def create_error_response(message: str, status_code: int = 400) -> JSONResponse:
    """
    Create a standardized error response.
    """
    response_data = {
        "success": False,
        "message": message,
        "data": None
    }
    return JSONResponse(content=response_data, status_code=status_code)


def format_response(data: Any, message: str = "Operation successful"):
    """
    Format a response with success wrapper.
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }