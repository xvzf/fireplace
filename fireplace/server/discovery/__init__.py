from sanic import Blueprint

discovery = Blueprint(
    "discovery", url_prefix="/discovery", strict_slashes=True)

from . import endpoint