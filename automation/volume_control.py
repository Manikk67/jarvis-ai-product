"""Windows volume control via pycaw — lazy initialization."""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

_volume = None
_init_failed = False


def _get_volume():
    global _volume, _init_failed

    if _init_failed:
        return None

    if _volume is not None:
        return _volume

    try:
        from ctypes import POINTER, cast

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        speakers = AudioUtilities.GetSpeakers()
        interface = speakers.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        _volume = cast(interface, POINTER(IAudioEndpointVolume))
        return _volume
    except Exception as exc:
        logger.error("Volume control unavailable: %s", exc)
        _init_failed = True
        return None


def volume_up(step: float = 0.1) -> str:
    vol = _get_volume()
    if not vol:
        return "Volume control is not available."

    current = vol.GetMasterVolumeLevelScalar()
    vol.SetMasterVolumeLevelScalar(min(current + step, 1.0), None)
    return "Volume increased."


def volume_down(step: float = 0.1) -> str:
    vol = _get_volume()
    if not vol:
        return "Volume control is not available."

    current = vol.GetMasterVolumeLevelScalar()
    vol.SetMasterVolumeLevelScalar(max(current - step, 0.0), None)
    return "Volume decreased."


def set_volume_percent(percent: int) -> str:
    vol = _get_volume()
    if not vol:
        return "Volume control is not available."

    percent = max(0, min(100, percent))
    vol.SetMasterVolumeLevelScalar(percent / 100.0, None)
    return f"Volume set to {percent}%."


def parse_volume_command(command: str) -> Optional[str]:
    """Handle 'volume up to 50%' or 'volume down to 20%'."""
    match = re.search(r"volume\s+(?:up|down)\s+to\s+(\d+)\s*%?", command)
    if match:
        return set_volume_percent(int(match.group(1)))

    match = re.search(r"set\s+volume\s+(?:to\s+)?(\d+)\s*%?", command)
    if match:
        return set_volume_percent(int(match.group(1)))

    return None


def mute_volume() -> str:
    vol = _get_volume()
    if not vol:
        return "Volume control is not available."

    vol.SetMute(1, None)
    return "Volume muted."


def unmute_volume() -> str:
    vol = _get_volume()
    if not vol:
        return "Volume control is not available."

    vol.SetMute(0, None)
    return "Volume unmuted."
