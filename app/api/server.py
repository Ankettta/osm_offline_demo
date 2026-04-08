from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import WEB_DIR, DATA_DIR
from app.map_core.tile_routes import router as tile_router
from app.simulation.generator import generate_points
from app.simulation.scenarios import SCENARIOS
from app.analytics.density import build_density
from app.analytics.recommender import recommend, USER_POINTS

app = FastAPI()
app.include_router(tile_router)

app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")



@app.get("/", response_class=HTMLResponse)
def index():
    html_path = WEB_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})


@app.get("/routes")
def routes():
    return [route.path for route in app.routes]


@app.get("/debug-paths")
def debug_paths():
    return {
        "data_dir": str(DATA_DIR),
        "tiles_dir": str(DATA_DIR / "tiles"),
        "tiles_dir_exists": (DATA_DIR / "tiles").exists(),
        "web_dir": str(WEB_DIR),
        "web_dir_exists": WEB_DIR.exists(),
    }


@app.get("/scenarios")
def get_scenarios():
    return [{"key": key, "name": value["name"]} for key, value in SCENARIOS.items()]


@app.get("/analysis")
def analysis(
    scenario: str = Query(...),
    mode: str = Query("to_crowd"),
    user_key: str = Query("kazan_cathedral"),
):
    if scenario not in SCENARIOS:
        return JSONResponse(
            status_code=400,
            content={"error": "Некорректный сценарий"}
        )

    generated = generate_points(scenario)
    points = generated["points"]
    hotspots = build_density(points)
    recommendation = recommend(hotspots, mode=mode, user_key=user_key)

    return {
        "scenario": generated["scenario"],
        "scenario_name": generated["scenario_name"],
        "user_position": recommendation["user_position"],
        "points": points,
        "hotspots": hotspots[:8],
        "recommendation": recommendation,
    }


@app.get("/user-points")
def get_user_points():
    return [{"key": key, "name": value["name"]} for key, value in USER_POINTS.items()]