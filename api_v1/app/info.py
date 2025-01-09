import socket
import sys

from fastapi import APIRouter

router = APIRouter()

hostname = socket.gethostname()

version = f"{sys.version_info.major}.{sys.version_info.minor}"


@router.get(
    "",
    tags=["Info"],
)
async def info():
    return {
        "name": "cb_rf_api",
        "host": hostname,
        "version": f"Hello world! From FastAPI running on Uvicorn. Using Python {version}",
        "url": "http://localhost/openapi.json",
    }
