from pycaw.pycaw import AudioUtilities
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume

# ==========================================
# GET VOLUME OBJECT
# ==========================================

speakers = AudioUtilities.GetSpeakers()

interface = speakers.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(
    interface,
    POINTER(IAudioEndpointVolume)
)

# ==========================================
# VOLUME UP
# ==========================================

def volume_up():

    current = volume.GetMasterVolumeLevelScalar()

    volume.SetMasterVolumeLevelScalar(
        min(current + 0.1, 1.0),
        None
    )

# ==========================================
# VOLUME DOWN
# ==========================================

def volume_down():

    current = volume.GetMasterVolumeLevelScalar()

    volume.SetMasterVolumeLevelScalar(
        max(current - 0.1, 0.0),
        None
    )

# ==========================================
# MUTE
# ==========================================

def mute_volume():

    volume.SetMute(1, None)

# ==========================================
# UNMUTE
# ==========================================

def unmute_volume():

    volume.SetMute(0, None)