import logging
import json
import os
import data_receiver, data_writer, helpers
from influxdb_client import InfluxDBClient
import time

class portfolio:
    """This class represents a portfolio based on an isin file"""

    def __init__(self, influxdb_client, isin_file):
            with open(isin_file) as portfolio_file:
                logging.info("loading isin_file: "+ isin_file)
                self.portfolio_items = json.load(portfolio_file)
                self.influxdb_client = influxdb_client

    def save_security_price(self):
            # Calculate Metrics
            self.stockReturn=helpers.calculateReturn(self.stockCurrentPrice,self.stockBuyPrice)
            logging.info("Name: "+ self.stockName + ", CurrentPrice: " + str(self.stockCurrentPrice) + ", Return" + str(self.stockReturn))

            # Write to DB
            data_writer.writeStockPriceInflux(self.influxdb_client, self.stockName, self.stockCurrentPrice, self.stockQuantity)
            time.sleep(5)

    def get_current_price(self, security):
        #for security in self.portfolio:
        # READ INPUT
        self.stockSignal = security.get('signal')
        self.stockISIN = security.get('isin')
        self.stockQuantity = security['capital']['quantity']
        self.stockName = security['name']
        self.stockBuyPrice = security['capital']['buy_price']

        # QUERY APIs
        if self.stockSignal is not None:
            self.stockCurrentPrice=data_receiver.getInstrumentPriceSignal(self.stockSignal)
        else:
            self.stockCurrentPrice=data_receiver.getInstrumentPriceIsin(self.stockISIN)
