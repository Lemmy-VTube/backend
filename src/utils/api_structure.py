from typing import Any, Dict

from fastapi import Request
from fastapi.routing import APIRoute


def build_api_structure(request: Request, routes: list[APIRoute]) -> Dict[str, Any]:
    structure = {}
    seen_tag_paths = set()
    base_url = str(request.base_url).rstrip('/')

    for route in routes:
        if not isinstance(route, APIRoute):
            continue

        path = route.path
        methods = list(route.methods - {"HEAD", "OPTIONS"})
        summary = route.summary or ""
        description = route.description or ""
        tags = route.tags or []

        responses = {
            str(status_code): {
                "description": info.get("description", "")
            }
            for status_code, info in route.responses.items()
            if isinstance(info, dict)
        }

        endpoint_data = {
            "path": f"{base_url}{path}",
            "methods": methods,
            "summary": summary,
            "description": description,
            "responses": responses if responses else {},
            "dependencies": bool(route.dependant.dependencies)
        }

        parts = [part for part in path.strip("/").split("/") if part]
        current = structure
        full_path_so_far = ""

        for idx, part in enumerate(parts):
            key = "/" + part
            full_path_so_far += key
            is_last = idx == len(parts) - 1

            if key not in current:
                current[key] = {}

                if tags and full_path_so_far not in seen_tag_paths:
                    current[key]["tags"] = tags
                    seen_tag_paths.add(full_path_so_far)

            if is_last:
                current[key] = endpoint_data
            else:
                current = current[key]
    return structure