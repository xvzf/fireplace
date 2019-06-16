from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.route("/temperature")
async def get_temperature(request):
    """ Measures temp and returns it in json representation """
    return json({
        "temperature": 31.4
    })

if __name__ == "__main__":
    app.run(host="::", port=9000)
