import sanic
from sanic.response import text
import http3
from pprint import pprint

API_TOKEN = "892407626:AAGzvaeDJg7wBIkKuw36FAs8Q4SnwqBgef0"
CHAT_ID = -1001494458754

app = sanic.Sanic(__name__)

@app.route("/telegram", methods=["POST"])
async def dummy_telegram_alert(request):

    text_to_send = ""

    if request.json["event"] == "max_temp_exceeded":
        text_to_send = f"Achtung: Sensor {request.json['sensor']} hat die Maximaltemperatur überschritten!\n"
        text_to_send += f"Aktuelle Temperatur: {request.json['measured_temp']} (max: {request.json['threshold']})"
    else:
        text_to_send = f"Achtung: Sensor {request.json['sensor']} ist nicht erreichbar!"

    async with http3.AsyncClient() as client:
        try:
            resp = await client.get(
                f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
                , params={
                    "chat_id": CHAT_ID,
                    "text": text_to_send,
            })
            print(resp)
            if resp.status_code != 200:
                return text("FAILED")
            return text("OK")
        except ConnectionRefusedError:
            return text("FAILED")

app.run(host="::", port=9111)