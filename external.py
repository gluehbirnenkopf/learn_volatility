import urllib.request
import json

def getInstrumentPriceIsin(isin):
    with urllib.request.urlopen("https://component-api.wertpapiere.ing.de/api/v1/components/instrumentheader/{}".format(isin)) as url:
        data = json.loads(url.read().decode())
    return data['price']

def getInstrumentPriceSignal(signal):
    # initialize ticker for a stock
    ticker = yf.Ticker(signal)
    # get history of that stock
    history = ticker.history()
    # get historical data including last price (Close) and parse only this as last price
    last_quote = (history.tail(1)['Close'].iloc[0])
    return last_quote
