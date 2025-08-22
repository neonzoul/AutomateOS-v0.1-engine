from __future__ import annotations
from typing import Any, Dict

import httpx  # [[modern and easy-to-use HTTP client library.]]

from app.engine.nodes.base import BaseNode


class HttpRequestNode(BaseNode):
    """HTTP request node.

    Notes:
    - Does NOT raise for non-2xx responses; returns status_code, headers, json, text.
      This lets a downstream FilterNode decide pass/fail.
    - Accepts config keys: url (required), method (default GET), headers/header, params, json_body.
    """

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Read the configuration for this node from the self.config dictionary.
        url = self.config.get("url")
        method = self.config.get("method", "GET").upper()
        headers = self.config.get("headers") or self.config.get("header", {})
        params = self.config.get("params", {})
        json_body = self.config.get("json_body", {})

        if not url:
            print("HTTP Request Error: Error - URL is not defined in the config.")
            raise ValueError("URL is required for HttpRequestNode")

        print(f"HTTP Request Node: Executing {method} request to {url}")

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_body,
                )

                # Prepare the output data for the next node.
                try:
                    response_json: Any = response.json()
                except ValueError:
                    response_json = None

                output: Dict[str, Any] = {
                    "status_code": int(response.status_code),
                    "headers": dict(response.headers),
                    "json": response_json,
                    "text": response.text,
                }

                print(f"HTTP Request Node: Request completed. Status: {response.status_code}")
                return output

        except httpx.RequestError as e:
            # network / timeout / connection error
            print(f"HTTP Request Node: Request failed - {e}")
            raise


