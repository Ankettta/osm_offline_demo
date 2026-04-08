import random
from app.simulation.scenarios import SCENARIOS


def generate_points(scenario_key: str):
    if scenario_key not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_key}")

    scenario = SCENARIOS[scenario_key]
    points = []

    if "clusters" in scenario:
        for cluster in scenario["clusters"]:
            cx, cy = cluster["center"]
            count = cluster["count"]
            spread = cluster["spread"]

            for _ in range(count):
                lat = cx + random.uniform(-spread, spread)
                lon = cy + random.uniform(-spread, spread)

                points.append({
                    "lat": lat,
                    "lon": lon,
                    "weight": random.randint(5, 15)
                })

    if "lines" in scenario:
        for line in scenario["lines"]:
            start = line["start"]
            end = line["end"]
            count = line["count"]
            spread = line.get("spread", 0.00008)

            for _ in range(count):
                t = random.random()

                lat = start[0] + (end[0] - start[0]) * t
                lon = start[1] + (end[1] - start[1]) * t

                lat += random.uniform(-spread, spread)
                lon += random.uniform(-spread, spread)

                points.append({
                    "lat": lat,
                    "lon": lon,
                    "weight": random.randint(3, 10)
                })

    if "poi" in scenario:
        for poi in scenario["poi"]:
            cx, cy = poi["center"]
            count = poi["count"]
            spread = poi["spread"]

            for _ in range(count):
                lat = cx + random.uniform(-spread, spread)
                lon = cy + random.uniform(-spread, spread)

                points.append({
                    "lat": lat,
                    "lon": lon,
                    "weight": random.randint(6, 12)
                })

    return {
        "scenario": scenario_key,
        "scenario_name": scenario["name"],
        "points": points,
    }