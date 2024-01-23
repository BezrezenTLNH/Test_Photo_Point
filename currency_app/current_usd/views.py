import time
from datetime import datetime

import requests
from django.http import JsonResponse

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
MAX_REQUESTS = 10


def get_current_usd(request):
    # Get the current USD to RUB
    response = requests.get(API_URL)
    data = response.json()
    usd_to_rub_rate = data["rates"]["RUB"]

    # Save the current request in the history
    request.session.setdefault("history", []).append({
        "timestamp": datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        "usd_to_rub_rate": usd_to_rub_rate,
    })
    request.session["history"] = request.session["history"][-MAX_REQUESTS:]

    # Wait 10 seconds before the next request
    time.sleep(10)

    # Return actual rate in JSON format
    return JsonResponse({"USD_to_RUB_rate": usd_to_rub_rate,
                         "history": request.session.get("history", [])})
