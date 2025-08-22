from __future__ import annotations

import time
import json
from pathlib import Path
from typing import Optional, Any, Dict
import requests

API = "http://127.0.0.1:8000"
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def get_env_var(name: str) -> Optional[str]:
    if not ENV_PATH.exists():
        return None
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.split("=")[0] == name:
            return line.split("=", 1)[1].strip()
    return None


def login(email: str, password: str) -> str:
    r = requests.post(f"{API}/api/v1/login", data={"username": email, "password": password})
    r.raise_for_status()
    token = r.json().get("access_token")
    if not token:
        raise RuntimeError("No access_token in response")
    return token


def create_workflow(token: str, discord_url: str) -> int:
    body: Dict[str, Any] = {
        "name": "Stripe to Discord Bridge",
        "definition": {
            "steps": [
                {
                    "type": "http_request_node",
                    "config": {
                        "method": "POST",
                        "url": discord_url,
                        "json_body": {
                            "content": "\ud83c\udf89 New Sale! A payment of $10.00 was just successfully processed."
                        },
                    },
                }
            ]
        },
    }
    r = requests.post(
        f"{API}/api/v1/workflows",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps(body),
    )
    r.raise_for_status()
    wf = r.json()
    return int(wf["id"])  # type: ignore[index]


def trigger_workflow(wf_id: int) -> None:
    r = requests.post(f"{API}/api/v1/webhooks/{wf_id}")
    r.raise_for_status()


def poll_until_finished(token: str, wf_id: int, timeout_s: int = 30) -> str:
    start = time.time()
    while time.time() - start < timeout_s:
        r = requests.get(
            f"{API}/api/v1/workflows/{wf_id}/runs?limit=1",
            headers={"Authorization": f"Bearer {token}"},
        )
        r.raise_for_status()
        runs = r.json()
        if runs:
            status = runs[0].get("status")
            print("Run status:", status)
            if status in {"success", "failed"}:
                return status
        time.sleep(1)
    raise TimeoutError("Timed out waiting for run to finish")


def main() -> None:
    discord_url = get_env_var("DISCORD_NOTIFIER_URL")
    if not discord_url:
        raise RuntimeError("DISCORD_NOTIFIER_URL not found in .env")

    token = login("admin@example.com", "password1234")
    wf_id = create_workflow(token, discord_url)
    print("Created workflow id:", wf_id)

    trigger_workflow(wf_id)
    print("Triggered webhook job")

    final = poll_until_finished(token, wf_id)
    print("Final status:", final)


if __name__ == "__main__":
    main()
