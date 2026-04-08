from pathlib import Path
import sys


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()
WEB_DIR = BASE_DIR / "web"
DATA_DIR = BASE_DIR / "data"

HOST = "127.0.0.1"
PORT = 8000
APP_URL = f"http://{HOST}:{PORT}"