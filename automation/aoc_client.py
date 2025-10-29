from __future__ import annotations

import os
import ssl
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT = "AoC automation script"


class AoCClientError(RuntimeError):
    """Base exception for Advent of Code client failures."""


def read_session_token() -> str:
    token = os.environ.get("AOC_SESSION")
    if token:
        return token.strip()

    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("AOC_SESSION="):
                _, _, value = line.partition("=")
                if value:
                    return value.strip()

    raise AoCClientError("Missing AOC_SESSION environment variable or .env entry.")


def build_ssl_context() -> ssl.SSLContext:
    if os.environ.get("AOC_SKIP_TLS_VERIFY") == "1":
        return ssl._create_unverified_context()
    context = ssl.create_default_context()
    try:
        import certifi

        context.load_verify_locations(certifi.where())
    except ModuleNotFoundError:
        pass
    return context


def make_request(url: str, *, data: dict[str, str] | None = None) -> str:
    session = read_session_token()
    headers = {
        "Cookie": f"session={session}",
        "User-Agent": USER_AGENT,
    }
    payload: bytes | None = None
    method = "GET"
    if data is not None:
        payload = urlencode(data).encode("ascii")
        method = "POST"
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = Request(url, headers=headers, data=payload, method=method)
    context = build_ssl_context()

    with urlopen(request, context=context) as response:  # nosec - target is trusted
        if response.status != 200:
            raise AoCClientError(f"{method} {url} returned status {response.status}")
        return response.read().decode("utf-8")


def fetch_input(year: int, day: int) -> str:
    return make_request(f"https://adventofcode.com/{year}/day/{day}/input")


def submit_answer(year: int, day: int, level: int, answer: str) -> str:
    data = {"level": str(level), "answer": answer}
    return make_request(f"https://adventofcode.com/{year}/day/{day}/answer", data=data)
