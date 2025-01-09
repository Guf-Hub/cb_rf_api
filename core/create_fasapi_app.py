from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.responses import ORJSONResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

tags_metadata = [
    {
        "name": "CB RF",
        "description": "С помощью этих методов можно получить данные по курсам валют.",
        "externalDocs": {"url": "https://www.cbr.ru/development/SXML/"},
    },
]


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # startup
#     yield
#     # shutdown
#     await db_helper.dispose()


def register_static_docs_routes(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )


def create_app(create_custom_static_urls: bool = False) -> FastAPI:

    app = FastAPI(
        default_response_class=ORJSONResponse,
        title="CB RF API",
        description="This is a simple service",
        version="0.0.1",
        contact={
            "name": "Mikhail Nosaev",
            "email": "<nosaev.mihail@yandex.ru>",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        openapi_tags=tags_metadata,
        docs_url=None if create_custom_static_urls else "/",  # "/docs",
        # redoc_url=None if create_custom_static_urls else "/",  # "/redoc",
    )

    if create_custom_static_urls:
        register_static_docs_routes(app)

    return app
