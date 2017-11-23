import requests

def findCoinMarketCapPrice(symbol):
    searchSymbol = symbol.upper()
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/')
    result = r.json()

    filtered = [x for x in result if x['symbol'] == searchSymbol]

    count = len(filtered)

    if count != 0:
        usd = format(float(filtered[0]["price_usd"]), ",.2f")
        btc = filtered[0]["price_btc"]

        volumeUSD = filtered[0]["24h_volume_usd"]
        percentChange = format(float(filtered[0]["percent_change_24h"]), ",.2f")
        marketCapUSD = "$" + format(float(filtered[0]["market_cap_usd"]), ",.2f")

        message = searchSymbol + "/USD: " + str(usd) + "\n" + searchSymbol + "/BTC: " + str(btc) + "\n" + "Volume: " + str(volumeUSD) + "\n" + "Percent Change: " + percentChange + "%\nMarket Cap: " + str(marketCapUSD)

        print(message)
        return message

def findGlobalData():
    r = requests.get('https://api.coinmarketcap.com/v1/global/')

    result = r.json()

    totalMarketCapUSD = "$" + format(float(result["total_market_cap_usd"]), ",.2f")
    total24HoursVolumeUSD = "$" + format(float(result["total_24h_volume_usd"]), ",.2f")
    BTCPercentage = str(result["bitcoin_percentage_of_market_cap"])

    message = "Total Market Cap: " + totalMarketCapUSD + "\nTotal 24 Hours Volume: " + total24HoursVolumeUSD + "\nBTC Percentage of Market Cap: " + BTCPercentage + "%"

    print(message)
    return message
