from influxdb_client import InfluxDBClient
import os
import logging
import sys

import portfolio


if __name__ == "__main__":

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    influxdbClient = InfluxDBClient(
        url=os.getenv("DB_URL"),
        token=os.getenv("DB_TOKEN"),
        org=os.getenv("DB_ORG")
    )

    p = portfolio.portfolio(influxdbClient, "/home/pyrunner/portfolio.json")

    if os.getenv("LOOP") == "True":
        while True:
            logging.info("Running in loop mode...")
            for security in p.portfolio_items:
                p.get_current_price(security)
                p.save_security_price()
    else:
        for security in p.portfolio_items:
            p.get_current_price(security)
            p.save_security_price()
