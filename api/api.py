from flask import Flask, jsonify, request
from timetable import timetable
from user import UserRepo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

repo = UserRepo.load_users()

@app.route("/get_timetable/<intake_code>/<group_number>")
def get_timetable(intake_code, group_number):
    ignored_modules = request.args.getlist("ignored")
    print (ignored_modules)
    class_list = timetable.get_timetable(intake_code, group_number, ignored_modules)
    return jsonify(class_list)

@app.post("/auth/login")
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


if __name__ == '__main__':
    app.run(host="0.0.0.0")
