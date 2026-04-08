import threading
import time
import webbrowser
from urllib.request import urlopen
from urllib.error import URLError

import webview
import uvicorn

from app.api.server import app
from app.config import HOST, PORT, APP_URL


def run_api():
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


def wait_for_server(url: str, timeout: float = 10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urlopen(f"{url}/health") as response:
                if response.status == 200:
                    return True
        except URLError:
            time.sleep(0.2)
        except Exception:
            time.sleep(0.2)
    return False


if __name__ == "__main__":
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    if not wait_for_server(APP_URL):
        raise RuntimeError("API server did not start in time.")

    window = webview.create_window(
        title="OSM Offline Demo",
        url=APP_URL,
        width=1280,
        height=800
    )
    webview.start()