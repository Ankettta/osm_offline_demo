from collections import defaultdict

import numpy as np
from sklearn.cluster import DBSCAN


def build_density(points, eps=0.00045, min_samples=4):
    if not points:
        return []

    coords = np.array([[p["lat"], p["lon"]] for p in points])

    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(coords)

    clusters = defaultdict(list)

    for point, label in zip(points, labels):
        if label == -1:
            continue
        clusters[label].append(point)

    hotspots = []

    for _, cluster_points in clusters.items():
        lat = sum(p["lat"] for p in cluster_points) / len(cluster_points)
        lon = sum(p["lon"] for p in cluster_points) / len(cluster_points)
        score = sum(p.get("weight", 1) for p in cluster_points)

        hotspots.append({
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "score": score,
            "count": len(cluster_points),
        })

    hotspots.sort(key=lambda x: x["score"], reverse=True)
    return hotspots