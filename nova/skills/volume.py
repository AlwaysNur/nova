import subprocess

def set_volume(level: int):
    if not 0 <= level <= 10:
        return("Volume must be between 0 and 10")

    subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{level * 10}%"],
        check=True
    )

    return f"Volume set to {level} out of 10"