from typing import List

from fastapi import Request
from fastapi.routing import APIRoute


def get_endpoints_for_version(request: Request, routes: List[APIRoute], version: str) -> List[str]:
    endpoints = []
    for route in routes:
        if not isinstance(route, APIRoute):
            continue
        
        path = route.path
        base_url = str(request.base_url).rstrip('/')
        
        if version in path:
            endpoints.append(f"{base_url}{path}")
    return sorted(endpoints)