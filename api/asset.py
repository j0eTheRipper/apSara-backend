from flask import Blueprint, send_from_directory, make_response, Response
import pathlib

assets_bp = Blueprint("assets", __name__, url_prefix="/asset")
ASSETS_DIR = pathlib.Path(__file__).resolve().parent / "assets"

def secure_asset(response: Response):
    _ = response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; script-src 'self' ; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
    )

    return response


@assets_bp.route("/navigation_menu_page.html")
def navigation_menu_page():
    resp = make_response(send_from_directory(ASSETS_DIR, "navigation_menu_page.html"))
    return secure_asset(resp)

@assets_bp.route("/campus_navigation.html")
def campus_navigation():
    resp = make_response(send_from_directory(ASSETS_DIR, "campus_navigation.html"))
    return secure_asset(resp)
