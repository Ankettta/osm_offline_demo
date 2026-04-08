import math


USER_POINTS = {
    "kazan_cathedral": {
        "name": "У Казанского собора",
        "lat": 59.935181,
        "lon": 30.325008,
    },
    "metro_nevsky": {
        "name": "У метро Невский проспект",
        "lat": 59.935687,
        "lon": 30.327232,
    },
    "griboedov_embankment": {
        "name": "Набережная канала Грибоедова",
        "lat": 59.934048,
        "lon": 30.326970,
    },
}


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def direction_text(from_lat, from_lon, to_lat, to_lon):
    dlat = to_lat - from_lat
    dlon = to_lon - from_lon

    if abs(dlat) < 0.0002:
        return "восток" if dlon > 0 else "запад"

    if abs(dlon) < 0.0002:
        return "север" if dlat > 0 else "юг"

    if dlat > 0 and dlon > 0:
        return "северо-восток"
    if dlat > 0 and dlon < 0:
        return "северо-запад"
    if dlat < 0 and dlon > 0:
        return "юго-восток"
    return "юго-запад"


def build_vector(user_position, target):
    dx = round(target["lon"] - user_position["lon"], 6)
    dy = round(target["lat"] - user_position["lat"], 6)

    return {
        "from": {
            "lat": user_position["lat"],
            "lon": user_position["lon"],
        },
        "to": {
            "lat": target["lat"],
            "lon": target["lon"],
        },
        "dx": dx,
        "dy": dy,
    }


def recommend(hotspots, mode="to_crowd", user_key="kazan_cathedral"):
    user_position = USER_POINTS.get(user_key, USER_POINTS["kazan_cathedral"])

    user_lat = user_position["lat"]
    user_lon = user_position["lon"]

    if not hotspots:
        return {
            "mode": mode,
            "user_position": user_position,
            "text": "Недостаточно данных для рекомендации.",
            "vector": None,
        }

    if mode == "to_crowd":
        target = hotspots[0]
        dist = int(haversine_m(user_lat, user_lon, target["lat"], target["lon"]))
        direction = direction_text(user_lat, user_lon, target["lat"], target["lon"])

        text = (
            f"Наиболее активная зона находится примерно в {dist} м. "
            f"Направление: {direction}. "
            f"Рекомендуется двигаться к зоне с высокой концентрацией пользователей."
        )

        return {
            "mode": mode,
            "user_position": user_position,
            "target": target,
            "text": text,
            "vector": build_vector(user_position, target),
        }

    # avoid_crowd
    calmer = sorted(hotspots, key=lambda x: (x["score"], -x["count"]))
    target = calmer[0]
    dist = int(haversine_m(user_lat, user_lon, target["lat"], target["lon"]))
    direction = direction_text(user_lat, user_lon, target["lat"], target["lon"])

    text = (
        f"Найден менее загруженный участок примерно в {dist} м. "
        f"Направление: {direction}. "
        f"Рекомендуется обойти зоны скопления через более спокойную область."
    )

    return {
        "mode": mode,
        "user_position": user_position,
        "target": target,
        "text": text,
        "vector": build_vector(user_position, target),
    }