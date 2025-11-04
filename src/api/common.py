from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.config import config
from src.utils.api_structure import build_api_structure
from src.utils.endpoints import get_endpoints_for_version
from src.utils.exceptions import error_response_http, success_response
from src.utils.responses import custom_responses

router = APIRouter(tags=["common"])


@router.get(
    "/",
    summary="API Information",
    description="Returns complete API information",
    responses=custom_responses
)
async def get_api_info(request: Request) -> JSONResponse:
    try:
        return success_response(
            data={
                "info": {
                    "developer": config.DEVELOPER_USERNAME,
                    "github": config.GITHUB_URL,
                    "docs": f"{request.base_url}docs",
                    "swagger": f"{request.base_url}swagger",
                    "redoc": f"{request.base_url}redoc",
                    "api_url": str(request.base_url)
                },
                "api_structure": build_api_structure(request, request.app.routes)
            },
            message="API structure successfully retrieved"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))


@router.get(
    '/versions',
    summary="API Versions",
    description="Returns information about all API versions with changes and endpoints",
    responses=custom_responses
)
async def get_versions_api(request: Request) -> JSONResponse:
    try:
        versions = config.API_VERSIONS
        for version_info in versions:
            version = version_info["version"]
            version_info["endpoints"] = get_endpoints_for_version(
                request, request.app.routes, version
            )
        return success_response(
            data={"versions": versions},
            message="API versions successfully retrieved"
        )
    except Exception as e:
        raise error_response_http(500, "Internal Server Error", str(e))