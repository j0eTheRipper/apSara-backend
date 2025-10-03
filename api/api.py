from flask import Flask, jsonify, request
from timetable import timetable
from auth import auth_bp
from asset import assets_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)
app.register_blueprint(assets_bp)

@app.route("/get_timetable/<intake_code>/<group_number>")
def get_timetable(intake_code, group_number):
    ignored_modules = request.args.getlist("ignored")
    print (ignored_modules)
    class_list = timetable.get_timetable(intake_code, group_number, ignored_modules)
    return jsonify(class_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
