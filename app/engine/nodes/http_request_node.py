from __future__ import annotations
from typing import Any, Dict

import httpx # [[modern and easy-to-use HTTP client library.]]

from app.engine.nodes.base import BaseNode

# It ingerites from BaseNode, fulfilling plugin "contract"
# [[The class name using CamelCase convention.]]
class HttpRequestNode(BaseNode):

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Makes an HTTP request based on the configuration and returns the response.
        """
        # Readt the configuration for this node from the self.config dictionary.
        url = self.config.get("url")
        method = self.config.get("method", "GET").upper() #[[Default to GET]]
        headers = self.config.get("header", {})
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

                # raises httpx.HTTPStatusError on non-2xx
                response.raise_for_status()

                # Prepare the output data for the next node.
                # parse JSON safely
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

                print(f"HTTP Request Node: Request successful. Status: {response.status_code}")
                return output

        except httpx.HTTPStatusError as e:
            # server responded with error status (raise_for_status)
            print(f"HTTP Request Node: HTTP error - {e}")
            raise
        except httpx.RequestError as e:
            # network / timeout / connection error
            print(f"HTTP Request Node: Request failed - {e}")
            raise


