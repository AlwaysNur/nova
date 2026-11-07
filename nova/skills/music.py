import time

from ytmusicapi import YTMusic
import subprocess

yt = YTMusic()

def search_song(query: str):
    results = yt.search(query, filter="songs", limit=5)

    return results


def play_song(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"

    process = subprocess.Popen([
        "mpv",
        "--input-ipc-server=" + "/tmp/nova-mpv-socket",
        "--no-video",
        "--really-quiet",
        "--no-terminal",
        url
    ])
    return(process)

def stop_music(process):
    process.terminate()
