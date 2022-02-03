import json
import time
from datetime import datetime
import os
import urllib.request

# logging libs
import logging
import sys
import yfinance as yf

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WritePrecision, SYNCHRONOUS, Point

class dataWriter:
    def writeStockPriceInflux(influxdbClient, name, price, quantity):
        volume = price * quantity
        p = Point("stock").tag("name", name).field("volume", volume).time(datetime.utcnow(),WritePrecision.MS)
        write_api = influxdbClient.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="marketdata", record=p)

class calculator:
    def calculateReturn(price, buy_price):
        percentage=(price-buy_price)/buy_price
        return round(percentage*100,2)

class dataReceiver:
    def __init__(self):
        logging.info("ENABLE_INFLUX: "+str(os.getenv("ENABLE_INFLUX")))
        #if os.getenv("ENABLE_INFLUX"):

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

if __name__ == "__main__":

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Initialize Influx DB...")

    influxdbClient = InfluxDBClient(
        url="http://localhost:8086",
        token="9283hdsiuh9843JHGGH9382lLPO!",
        org="moon"
    )

    while True:
        with open('data/portfolio.json') as data_file:
            logging.info("loading isin file...")
            portfolio = json.load(data_file)

            for security in portfolio:
                # READ INPUT
                stockSignal=security.get('signal')
                stockISIN=security.get('isin')
                stockQuantity=security['capital']['quantity']
                stockName=security['name']
                stockBuyPrice=security['capital']['buy_price']

                # QUERY APIs
                if stockSignal is not None:
                    stockCurrentPrice=dataReceiver.getInstrumentPriceSignal(stockSignal)
                else:
                    stockCurrentPrice=dataReceiver.getInstrumentPriceIsin(stockISIN)

                # Calculate Metrics
                stockReturn=calculator.calculateReturn(stockCurrentPrice,stockBuyPrice)
                logging.info(stockName + ":" + str(stockCurrentPrice) + "," + str(stockReturn))

                dataWriter.writeStockPriceInflux(influxdbClient, stockName, stockCurrentPrice, stockQuantity)

                time.sleep(5)
