from skills import music, volume, time

player = None

def play_music(query: str):
    global player
    stop_music()
    results = music.search_song(query)

    if not results:
        return "No matching songs found."

    song = results[0]

    player = music.play_song(song["videoId"])

    return {
        "status": "playing",
        "title": song["title"],
        "artist": song["artists"][0]["name"]
    }


def stop_music():
    global player

    if player is None or player.poll() is not None:
        return "Nothing is currently playing."

    player.terminate()
    player.wait()
    player = None

    return "Music stopped."


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "play_music",
            "description": "Search YouTube Music and play a requested song.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Song title and artist."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stop_music",
            "description": "Stop the currently playing music.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set the audio volume from 0 to 10.",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Volume level, from 0 (muted) to 10 (maximum)."
                    }
                },
                "required": ["level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "current_time",
            "description": "Get the current time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def execute_tool(name, arguments):
    available_tools = {
        "play_music": play_music,
        "stop_music": stop_music,
        "set_volume": volume.set_volume,
        "current_time": time.current_time
    }

    if name not in available_tools:
        return "Unknown tool."

    return available_tools[name](**arguments)