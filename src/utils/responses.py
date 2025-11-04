custom_responses: dict = {
    200: {
        "description": "Successful response with API structure",
        "content": {
            "application/json": {
                "example": {
                    "data": {
                        "...": { "...": "..." }
                    },
                    "message": "Successful response with API structure"
                }
            }
        },
    },
    400: {
        "description": "Bad request — invalid or missing parameters",
        "content": {
            "application/json": {
                "example": {
                    "error": "Bad Request",
                    "details": "Invalid or missing parameters"
                }
            }
        },
    },
    401: {
        "description": "Unauthorized — authentication required or invalid token",
        "content": {
            "application/json": {
                "example": {
                    "error": "Unauthorized",
                    "details": "Authentication required or invalid token"
                }
            }
        },
    },
    403: {
        "description": "Forbidden — user does not have permission to access this resource",
        "content": {
            "application/json": {
                "example": {
                    "error": "Forbidden",
                    "details": "You do not have permission to access this resource"
                }
            }
        },
    },
    404: {
        "description": "Not found — the requested resource does not exist",
        "content": {
            "application/json": {
                "example": {
                    "error": "Not Found",
                    "details": "The requested resource does not exist"
                }
            }
        },
    },
    422: {
        "description": "Unprocessable Entity — validation error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "username"],
                            "msg": "ensure this value has at least 3 characters",
                            "type": "value_error.any_str.min_length",
                            "ctx": {"limit_value": 3}
                        }
                    ]
                }
            }
        }
    },
    429: {
        "description": "Too Many Requests — rate limit exceeded",
        "content": {
            "application/json": {
                "example": {
                    "error": "Too Many Requests",
                    "details": "You have exceeded the allowed number of requests."
                }
            }
        },
    },
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {
                    "error": "Internal Server Error",
                    "details": "An unexpected error occurred"
                }
            }
        },
    },
}
