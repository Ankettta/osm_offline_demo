import math
import os
import time
import requests

# файл загрузки тайлов с OSM уже не актуален - получаем заблокированные тайлы, но оставлен
BASE_DIR = "data/tiles"

# Область вокруг Казанского собора, можно потом подправить
MIN_LON = 30.3180
MIN_LAT = 59.9315
MAX_LON = 30.3335
MAX_LAT = 59.9385

ZOOMS = [14, 15, 16, 17]

HEADERS = {
    "User-Agent": "osm-offline-hackathon-demo/1.0"
}


def deg2num(lat_deg: float, lon_deg: float, zoom: int):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    )
    return xtile, ytile


def download_tile(z: int, x: int, y: int):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"

    path = os.path.join(BASE_DIR, str(z), str(x))
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, f"{y}.png")

    if os.path.exists(file_path):
        return False

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        f.write(response.content)

    return True


def main():
    total = 0
    downloaded = 0

    for z in ZOOMS:
        x_min, y_max = deg2num(MIN_LAT, MIN_LON, z)
        x_max, y_min = deg2num(MAX_LAT, MAX_LON, z)

        print(f"\nZoom {z}")
        print(f"x: {x_min}..{x_max}, y: {y_min}..{y_max}")

        for x in range(min(x_min, x_max), max(x_min, x_max) + 1):
            for y in range(min(y_min, y_max), max(y_min, y_max) + 1):
                total += 1
                try:
                    was_downloaded = download_tile(z, x, y)
                    if was_downloaded:
                        downloaded += 1
                        print(f"Downloaded {z}/{x}/{y}")
                    else:
                        print(f"Skipped {z}/{x}/{y}")
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Failed {z}/{x}/{y}: {e}")

    print("\nDone")
    print(f"Checked: {total}")
    print(f"Downloaded new: {downloaded}")


if __name__ == "__main__":
    main()