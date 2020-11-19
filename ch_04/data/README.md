# About the data

| File | Description | Source |
| --- | --- | --- |
| `dirty_data.csv` | Dirty weather data from the *Handling duplicate, missing, or invalid data* section in *Chapter 3, Data Wrangling with Pandas* | Adapted from the NCEI API's GHCND dataset |
| `fb_2018.csv` | Facebook stock's opening, high, low, and closing price daily, along with volume traded for 2018. | The `stock_analysis` package (see *Chapter 7, Financial Analysis &ndash; Bitcoin and the Stock Market*). |
| `fb_week_of_may_20_per_minute.csv` | Facebook stock's opening, high, low, and closing price per minute, along with volume traded for May 20, 2019 through May 24, 2019. | https://www.nasdaq.com/symbol/fb/interactive-chart |
| `melted_stock_data.csv` | The contents of `fb_week_of_may_20_per_minute.csv` melted into a single column for the price and another for the timestamp. | Adapted from https://www.nasdaq.com/symbol/fb/interactive-chart |
| `nyc_weather_2018.csv` | Long format weather data for New York City across various stations. | The NCEI API's GHCND dataset. |
| `stocks.db` | The `fb_prices` and `aapl_prices` tables contain the stock prices for Facebook and Apple, respectively, for May 20, 2019 through May 24, 2019. Facebook is at a minute granularity, whereas Apple has timestamps that include (fictitious) seconds. | Facebook data: https://www.nasdaq.com/symbol/fb/interactive-chart Apple data, adapted from: https://www.nasdaq.com/symbol/aapl/interactive-chart |
| `weather_by_station.csv` | Long format weather data for New York City across various stations, along with station information. | The NCEI API's GHCND dataset and the `stations` endpoint. |
| `weather_stations.csv` | Information on all the stations providing weather data for New York City. | The NCEI API's `stations` endpoint. |
| `weather.db` | The `weather` table contains New York City weather data, while the `stations` table contains information on the stations. | The NCEI API's GHCND dataset and the `stations` endpoint. |
