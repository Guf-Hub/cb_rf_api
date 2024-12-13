import uvicorn
from api_v1 import router as router_v1

from core.create_fasapi_app import create_app
from core.config import settings

app = create_app(create_custom_static_urls=False)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run(**settings.uvicorn.uvicorn_kwargs)
