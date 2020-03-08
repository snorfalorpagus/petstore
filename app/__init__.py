from pathlib import Path

import connexion
import aiohttp
from aiohttp import web
from aiohttp.web import Request
from aiohttp.web_exceptions import HTTPPermanentRedirect

from .data_types import BaseType
from .connexion_utils import load_api_spec, AppResolver

__version__ = "1.0.0"


async def swagger_ui_redirect(request: Request):
    location = "/ui/"
    raise HTTPPermanentRedirect(location=location)


def create_app():
    app = connexion.AioHttpApp(__name__, port=5000, specification_dir="", only_one_api=True)

    spec_path = Path(__file__).parent / "api-spec.yaml"
    spec, _ = load_api_spec(spec_path, version=__version__, components=[BaseType])

    app.add_api(
        spec, options={"swagger_ui": True}, resolver=AppResolver(), pass_context_arg_name="request",
    )
    aiohttp_app: aiohttp.web.Application = app.app
    aiohttp_app.add_routes([web.get("/", swagger_ui_redirect)])

    return app
