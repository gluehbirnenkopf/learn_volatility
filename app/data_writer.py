import logging
from influxdb_client.client.write_api import WritePrecision, SYNCHRONOUS, Point
from datetime import datetime
import os

def writeStockPriceInflux(influxdb_client, name, price, quantity):
    volume = price * quantity
    p = Point("stock").tag("name", name).field("volume", volume).time(datetime.utcnow(),WritePrecision.MS)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    # write using point structure
    try:
        write_api.write(bucket="marketdata", record=p)
    except Exception as e:
        logging.error("Database not ready or not reachable." + e)
