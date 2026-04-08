from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import DATA_DIR

router = APIRouter()

TILES_DIR = DATA_DIR / "tiles"


@router.get("/tiles/{z}/{x}/{y}.png")
def get_tile(z: int, x: int, y: int):
    tile_path = TILES_DIR / str(z) / str(x) / f"{y}.png"

    if not tile_path.exists():
        raise HTTPException(status_code=404, detail="Tile not found")

    return FileResponse(tile_path)