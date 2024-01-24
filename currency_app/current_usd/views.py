from datetime import datetime

import requests
from django.http import JsonResponse

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
MAX_REQUESTS = 10
TIME_INTERVAL = 10


def get_current_usd(request):
    # Get the current USD to RUB
    response = requests.get(API_URL)
    data = response.json()
    usd_to_rub_rate = data["rates"]["RUB"]
    current_time = datetime.now()
    last_request_time = None

    #  Getting the time of the last request from the history, if it is not empty
    if request.session.get("history"):
        last_request_time = datetime.strptime(request.session["history"][-1]["timestamp"], '%d.%m.%Y %H:%M:%S')

    # Checking the time difference between the current request and the last request
    if not last_request_time or (current_time - last_request_time).seconds >= TIME_INTERVAL:
        # Saving the current request to history
        request.session.setdefault("history", []).append({
            "timestamp": current_time.strftime('%d.%m.%Y %H:%M:%S'),
            "usd_to_rub_rate": usd_to_rub_rate,
        })
        request.session["history"] = request.session["history"][-MAX_REQUESTS:]

    # Return actual rate in JSON format
    return JsonResponse({"USD_to_RUB_rate": usd_to_rub_rate,
                         "history": request.session.get("history", [])})
