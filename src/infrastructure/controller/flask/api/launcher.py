from flask import jsonify, Blueprint


api_launcher = Blueprint("api_launcher", __name__)


@api_launcher.route("/", methods=["GET"])
def hello():
    foo = "bar"

    return jsonify(message="Hello world {}".format(foo)), 200
