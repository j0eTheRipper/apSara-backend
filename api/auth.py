from flask import Blueprint, jsonify, request
from user import UserRepo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
repo = UserRepo.load_users()

@auth_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    apkey = body.get("apkey", "").strip()
    password = body.get("password", "")

    # print(apkey, password)

    user = repo.get_by_apkey(apkey)
    # print(user)
    if not user or user.password != password:
        return jsonify({"error": {"message": "Invalid Credintials"}})

    # create a session token maybe a jwt for our case and LET HIM IN
    # we can include the intake and grouping in the token as well instead of user input from frontend
    return jsonify({"success": {"message": "LOGIN SUCCESSFULL"}})

