# Financial Market Crawler

Python based app to crawl financial securities using ING and Yahoo Finance APIs. Persists into influxdb time-series database.

### Quickstart
Use `portfolio.json` to configure individual securities based on ISIN or Ticker Symbol.
```
docker-compose up
```

Influx DB authentication and configuration parameters are changed via `compose.yml`. Crawler provides 2 run modes using the `LOOP` environment variable to choose wheter data should be queried infinte or only once.
