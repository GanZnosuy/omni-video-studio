"""
Centralized Autonomous Gemini Cookie Sync & WebAPI Bridge.
Silently harvests, validates, and propagates Gemini Web cookies across Antigravity,
NEXUS Agent, and AI video pipelines without requiring manual user intervention.
"""

import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger("gemini_cookie_sync")

CONFIG_DIR = Path(os.environ.get("GEMINI_CONFIG_DIR", Path.home() / ".gemini" / "config"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
GLOBAL_COOKIE_FILE = CONFIG_DIR / "gemini_cookies.json"

LOCAL_ENV_FILE = Path(os.environ.get("LOCAL_ENV_FILE", ".env"))


async def harvest_cookies_from_cdp(cdp_url: str = "http://localhost:9222") -> Optional[Dict[str, str]]:
    """
    Connects to running Chrome instance via CDP and extracts live Google/Gemini session cookies.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.warning("Playwright is not available for CDP harvesting.")
        return None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            if not browser.contexts:
                return None
            context = browser.contexts[0]
            cookies = await context.cookies([
                "https://gemini.google.com",
                "https://google.com",
                "https://accounts.google.com"
            ])
            cookie_dict = {c["name"]: c["value"] for c in cookies}

            psid = cookie_dict.get("__Secure-1PSID")
            psidts = cookie_dict.get("__Secure-1PSIDTS")
            psidcc = cookie_dict.get("__Secure-1PSIDCC")
            psidrts = cookie_dict.get("__Secure-1PSIDRTS")

            if psid and psidts:
                res = {
                    "GEMINI_SECURE_1PSID": psid,
                    "GEMINI_SECURE_1PSIDTS": psidts,
                }
                if psidcc:
                    res["GEMINI_SECURE_1PSIDCC"] = psidcc
                if psidrts:
                    res["GEMINI_SECURE_1PSIDRTS"] = psidrts
                return res
            return None
    except Exception as e:
        logger.debug(f"CDP harvesting failed on {cdp_url}: {e}")
        return None


def read_cached_cookies() -> Dict[str, str]:
    """Reads previously saved cookies from disk."""
    if not GLOBAL_COOKIE_FILE.exists():
        return {}
    try:
        data = json.loads(GLOBAL_COOKIE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception as e:
        logger.error(f"Failed to read cached cookies: {e}")
    return {}


def save_cached_cookies(cookies: Dict[str, str]) -> None:
    """Saves valid cookies to the centralized JSON file."""
    try:
        GLOBAL_COOKIE_FILE.write_text(json.dumps(cookies, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"Updated centralized cookies at {GLOBAL_COOKIE_FILE}")
    except Exception as e:
        logger.error(f"Failed to write cached cookies: {e}")


def sync_to_env_file(env_file_path: Path, cookies: Dict[str, str]) -> bool:
    """Updates or injects GEMINI_SECURE_* variables into a specific .env file."""
    if not env_file_path.exists():
        return False

    try:
        content = env_file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        found_keys = set()

        for line in lines:
            stripped = line.strip()
            matched = False
            for k, v in cookies.items():
                if stripped.startswith(f"{k}=") or stripped.startswith(f"export {k}="):
                    prefix = "export " if stripped.startswith("export ") else ""
                    new_lines.append(f"{prefix}{k}={v}")
                    found_keys.add(k)
                    matched = True
                    break
            if not matched:
                new_lines.append(line)

        # Append any new keys that were missing
        for k, v in cookies.items():
            if k not in found_keys:
                new_lines.append(f"{k}={v}")

        env_file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        logger.info(f"Successfully synced cookies to {env_file_path.name}")
        return True
    except Exception as e:
        logger.error(f"Error updating {env_file_path}: {e}")
        return False


async def auto_sync() -> bool:
    """
    Main entrypoint:
    1. Try to harvest from live Chrome CDP session.
    2. Fall back to cached cookies.
    3. Propagate to local .env file.
    """
    cookies = await harvest_cookies_from_cdp()
    if cookies:
        save_cached_cookies(cookies)
    else:
        cookies = read_cached_cookies()

    if not cookies or "GEMINI_SECURE_1PSID" not in cookies:
        logger.warning("No valid Gemini cookies found via CDP or cache.")
        return False

    if LOCAL_ENV_FILE.exists():
        sync_to_env_file(LOCAL_ENV_FILE, cookies)
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    success = asyncio.run(auto_sync())
    sys.exit(0 if success else 1)
