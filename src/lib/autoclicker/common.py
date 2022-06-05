import os
import enum

APP_NAME = "AutoClicker"
VERSION = "1.1.0.0"
AUTHOR = "Michael Canady"

ICON_FILE = ""

LOG_FILE = f"{os.environ.get('temp')}\AutoClicker\logs\my_app.log"

def get_required_paths() -> None:
    required_paths = [LOG_FILE]

    for path in required_paths:
        if not os.path.exists(path):
            print(f"{path} does not exist")

class Repeat(enum.IntEnum):
    finite = 1
    infinite = 2

class Location(enum.IntEnum):
    fixed = 1
    current = 2