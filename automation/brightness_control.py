"""Windows screen brightness control via WMI."""

import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


def _get_brightness() -> Optional[int]:
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness "
                "-ErrorAction SilentlyContinue | Select-Object -First 1).CurrentBrightness",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        value = result.stdout.strip()
        if value.isdigit():
            return int(value)
    except (subprocess.SubprocessError, OSError) as exc:
        logger.warning("Could not read brightness: %s", exc)
    return None


def _set_brightness(level: int) -> bool:
    level = max(0, min(100, level))
    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods "
                f"-ErrorAction SilentlyContinue | Select-Object -First 1)"
                f".WmiSetBrightness(1, {level})",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return True
    except (subprocess.SubprocessError, OSError) as exc:
        logger.warning("Could not set brightness: %s", exc)
        return False


def brightness_up(step: int = 10) -> str:
    current = _get_brightness()
    if current is None:
        return "Brightness control is not available on this display."
    new_level = min(100, current + step)
    if _set_brightness(new_level):
        return f"Brightness set to {new_level}%."
    return "Failed to adjust brightness."


def brightness_down(step: int = 10) -> str:
    current = _get_brightness()
    if current is None:
        return "Brightness control is not available on this display."
    new_level = max(0, current - step)
    if _set_brightness(new_level):
        return f"Brightness set to {new_level}%."
    return "Failed to adjust brightness."
