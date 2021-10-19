from flask import Flask, jsonify, request
from http import HTTPStatus


URL = "https://exponea-engineering-assignment.appspot.com/api/work"
app = Flask(__name__)


@app.route("/api/all", methods=["POST"])
def all_responses():
    if not request.json:
        return jsonify({"error": "empty payload"}), HTTPStatus.BAD_REQUEST

    time = request.json.get("time")
    responses = get_all_responses(time)

    if not responses:
        return HTTPStatus.BAD_REQUEST
    
    return jsonify(responses), HTTPStatus.OK


@app.route("/api/first", methods=["POST"])
def first_response():
    pass


if __name__ == '__main__':
    app.run(debug=True)
