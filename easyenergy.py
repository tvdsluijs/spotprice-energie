import requests
from dateutil import parser
from datetime import datetime

def EasyEnergy():
    now = datetime.now()
    startTimestamp = now.strftime("%Y-%m-%dT00:00:00.000Z")
    endTimestamp = now.strftime("%Y-%m-%dT23:59:00.000Z")

    if int(now.strftime("%H")) > 15:
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        startTimestamp = tomorrow.strftime("%Y-%m-%dT00:00:00.000Z")
        endTimestamp = tomorrow.strftime("%Y-%m-%dT23:59:00.000Z")

    url = f"https://mijn.easyenergy.com/nl/api/tariff/getapxtariffs?startTimestamp={startTimestamp}&endTimestamp={endTimestamp}&grouping="
    r = requests.get(url)

    print(f"{'Return Tariff':<13} {'Usage Tariff':<12} {'Date':<10} {'Time':<5}")

    for et in r.json():
        d = et['Timestamp']
        dt = parser.parse(d)
        print(f"{et['TariffReturn']:13.5f}", f"{et['TariffUsage']:12.7f}", dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M') )


if __name__ == "__main__":
    EasyEnergy()