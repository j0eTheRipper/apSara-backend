from flask import Flask, jsonify
import timetable


app = Flask(__name__)


@app.route("/get_timetable/<intake_code>/<group_number>")
def get_timetable(intake_code, group_number):
    class_list = timetable.get_timetable(intake_code, group_number)
    return jsonify(class_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
