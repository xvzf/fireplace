import flask
from pprint import pprint

app = flask.Flask(__name__)

@app.route("/email", methods=["POST"])
def dummy_mail_alert():
    pprint(flask.request.json)
    return "OK"

app.run(host="::", port=9111)
