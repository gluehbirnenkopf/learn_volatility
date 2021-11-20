import json
import time
from datetime import datetime
import os

import yfinance as yf
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WritePrecision, SYNCHRONOUS, Point


class TickerData:
    def __init__(self):
        if "ENABLE_INFLUX" in os.environ:
            self.influxdbClient = InfluxDBClient(
                url="http://localhost:8086",
                token=os.environ.get('INFLUX_TOKEN'),
                org="my-org"
            )

    def run(self):
        while True:
            with open('data/data.json') as data_file:
                print("loading data file...")
                data = json.load(data_file)
                for action in data:
                    ticker = yf.Ticker(action['signal'])
                    history = ticker.history()
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

                    print("Writing data:"+action['name']+":"+str(last_quote))

                    if "ENABLE_INFLUX" in os.environ:
                        p = Point("stock").tag("name", action['name']).field("price", last_quote).time(datetime.utcnow(),
                                                                                                      WritePrecision.MS)
                        write_api = self.influxdbClient.write_api(write_options=SYNCHRONOUS)

                        # write using point structure
                        write_api.write(bucket="ccc", record=p)

                    time.sleep(20)


if __name__ == "__main__":
    ticker = TickerData()
    ticker.run()