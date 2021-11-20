import json
import time
from datetime import datetime
import os

# logging libs
import logging
import sys

import yfinance as yf
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WritePrecision, SYNCHRONOUS, Point


class TickerData:
    def __init__(self):
        logging.info("ENABLE_INFLUX: "+str(os.getenv("ENABLE_INFLUX")))
        if os.getenv("ENABLE_INFLUX"):
            logging.info("Initialize Influx DB...")
            self.influxdbClient = InfluxDBClient(
                url="http://localhost:8086",
                token=os.getenv('INFLUX_TOKEN'),
                org="ccc"
            )
            logging.info("Initialize Influx DB successfull")

    def writeStockPriceInflux(self, name, price):
        p = Point("stock").tag("name", name).field("price", price).time(datetime.utcnow(),WritePrecision.MS)
        write_api = self.influxdbClient.write_api(write_options=SYNCHRONOUS)

        # write using point structure
        logging.info("db write")
        write_api.write(bucket="ccc", record=p)

    def run(self):
        while True:
            with open('data/data.json') as data_file:
                logging.info("loading data file...")
                data = json.load(data_file)

                for action in data:
                    # initialize ticker for a stock
                    ticker = yf.Ticker(action['signal'])
                    # get history of that stock
                    history = ticker.history()
                    # get historical data including last price (Close) and parse only this as last price
                    last_quote = (history.tail(1)['Close'].iloc[0])
                    json_body = [{
                        "measurement": "share_price",
                        "tags": {
                            "name": action['name']
                        },
                        "fields": {
                            "price": last_quote
                        }
                    }, {
                        "measurement": "capital",
                        "tags": {
                            "name": action['name'],
                        },
                        "fields": {
                            "quantity": action['capital']['quantity'],
                            "buy_price":
                                action['capital']['buy_price']
                        }
                    }]

                    logging.info("Writing data:"+action['name']+":"+str(last_quote))

                    if "ENABLE_INFLUX" in os.environ:
                        self.writeStockPriceInflux(action['name'], last_quote)

                    time.sleep(20)


if __name__ == "__main__":

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    dataSource = TickerData()
    dataSource.run()