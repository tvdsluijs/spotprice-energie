import requests
import sys
from datetime import datetime, timedelta
import csv

def FrankEnergy():
    now = datetime.now()

    yesterday = datetime.now() + timedelta(days=-1)
    startdate = yesterday.strftime("%Y-%m-%d")
    enddate = now.strftime("%Y-%m-%d")

    if int(now.strftime("%H")) > 15:
        tomorrow = datetime.now() + timedelta(days=2)
        startdate = now.strftime("%Y-%m-%d")
        enddate = tomorrow.strftime("%Y-%m-%d")

    headers = { "content-type":"application/json" }

    query = f"""query MarketPrices {{
        marketPricesElectricity(startDate: "{startdate}", endDate: "{enddate}") {{
        till
        from
        marketPrice
        priceIncludingMarkup
        }}
        marketPricesGas(startDate: "{startdate}", endDate: "{enddate}") {{
        from
        till
        marketPrice
        priceIncludingMarkup
    }}
    }}"""


    response = requests.post('https://graphcdn.frankenergie.nl', json={'query': query}, headers=headers)
    data = response.json()

    frank_electra_file = "frank_electra.csv"
    frank_gas_file = "frank_gas.csv"

    frank_headers = ['till', 'from', 'marketPrice', 'priceIncludingMarkup']

    with open(frank_electra_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = frank_headers)
        writer.writeheader()
        writer.writerows(data['data']['marketPricesElectricity'])

    with open(frank_gas_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = frank_headers)
        writer.writeheader()
        writer.writerows(data['data']['marketPricesGas'])

    for electra in data['data']['marketPricesElectricity']:
       print(electra['till'], electra['from'], electra['marketPrice'], electra['priceIncludingMarkup'])

    for gas in data['data']['marketPricesGas']:
        print(gas['till'], gas['from'],gas['marketPrice'], gas['priceIncludingMarkup'])


if __name__ == "__main__":
    FrankEnergy()