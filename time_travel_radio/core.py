# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['get_device_id', 'DecadesPlayer', 'play']

# Cell
from fastcore.all import *
from typing import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Cell
def get_device_id(devices: Dict, name: str):
    if len(devices["devices"]) == 0: raise ValueError("No active devices")
    for d in devices["devices"]:
        if d["name"] == name:
            return d["id"]
    raise ValueError(f"No active device named {name}")

# Cell
class DecadesPlayer:
    """Plays music on Raspberry Pi."""
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    playlists = {
        '1920s': 'spotify:playlist:7olpTqGzGrYuI76ZBlCLgs',
        '1930s': 'spotify:playlist:6yY2tBY8976eFqsOIlBA0b',
        '1940s': 'spotify:playlist:245g9upOJ2BLTCcKeFyRDf',
        '1950s': 'spotify:playlist:5TLQjeDvm4igfsJgi6FaF7',
        '1960s': 'spotify:playlist:37i9dQZF1DXaKIA8E7WcJj',
        '1970s': 'spotify:playlist:37i9dQZF1DWTJ7xPn4vNaz',
        '1980s': 'spotify:playlist:37i9dQZF1DX4UtSsGT1Sbe',
        '1990s': 'spotify:playlist:37i9dQZF1DXbTxeAdrVG2l',
        '2000s': 'spotify:playlist:2f6tXtN0XesjONxicAzMIw',
        '2010s': 'spotify:playlist:3FeewjLi5LMzIpV4h35QEz'
    }

    def __init__(self, device_name: str):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=DecadesPlayer.scope))
        self.device = get_device_id(self.sp.devices(), device_name)

    def play_music(self, decade: str):
        """Plays `decade` on device."""
        if decade not in self.playlists: raise KeyError(f"Invalid decade: {decade}")
        self.sp.start_playback(device_id=self.device, context_uri=DecadesPlayer.playlists[decade])

    def change_volume(self, volume: int): self.sp.volume(volume, device_id=self.device)

# Cell
@call_parse
def play(
    device_name: Param("Name of device", type=str)="Brandon's Raspberry Pi"
):
    """Creates a `DecadesPlayer` and forever loops controls :)."""
    player = DecadesPlayer(device_name)

    while True:
        action = input("What to change the (d)ecade or the (v)olume?")
        if action == "d":
            decade = input("Which decade?")
            try: player.play_music(decade)
            except KeyError: print("Invalid decade")
        elif action == "v":
            volume = int(input("What volume?"))
            player.change_volume(volume)
        else: print("Invalid choice")