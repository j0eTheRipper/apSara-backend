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

@assets_bp.route("/<path:filename>")
def serve_static(filename):
    try:
        resp = make_response(send_from_directory(ASSETS_DIR, filename))
        if filename.endswith('.css'):
            resp.headers['Content-Type'] = 'text/css'
        elif filename.endswith('.js'):
            resp.headers['Content-Type'] = 'application/javascript'
        elif filename.endswith('.png'):
            resp.headers['Content-Type'] = 'image/png'
        elif filename.endswith(('.jpg', '.jpeg')):
            resp.headers['Content-Type'] = 'image/jpeg'
        elif filename.endswith('.gif'):
            resp.headers['Content-Type'] = 'image/gif'
        elif filename.endswith('.webp'):
            resp.headers['Content-Type'] = 'image/webp'
        return resp
    except FileNotFoundError:
        return f"File not found: {filename}", 404
