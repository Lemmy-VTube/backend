from fastapi import HTTPException
from fastapi.responses import JSONResponse


def error_response_http(status_code: int, error: str, details: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "error": error,
            "details": details
        }
    )


def error_response_json(status_code: int, error: str, details: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "details": details
        }
    )


def success_response(
    data: dict, 
    message: str = "Successful response with API structure"
) -> JSONResponse:
    return JSONResponse(
        content={
            "data": data,
            "message": message
        },
        status_code=200
    )


def forbidden_error(details: str = "Access denied") -> HTTPException:
    return error_response_http(403, "Forbidden", details)


def too_many_requests_error(details: str = "Rate limit exceeded") -> JSONResponse:
    return error_response_json(429, "Too Many Requests", details)