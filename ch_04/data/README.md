# About the data

| File | Description | Source |
| --- | --- | --- |
| `dirty_data.csv` | Dirty weather data from the *Handling duplicate, missing, or invalid data* section in *Chapter 3, Data Wrangling with Pandas* | Adapted from the NCEI API's GHCND dataset |
| `fb_2018.csv` | Facebook stock's opening, high, low, and closing price daily, along with volume traded for 2018. | The `stock_analysis` package (see *Chapter 7, Financial Analysis &ndash; Bitcoin and the Stock Market*). |
| `fb_week_of_may_20_per_minute.csv` | Facebook stock's opening, high, low, and closing price per minute, along with volume traded for May 20, 2019 through May 24, 2019. | Nasdaq |
| `melted_stock_data.csv` | The contents of `fb_week_of_may_20_per_minute.csv` melted into a single column for the price and another for the timestamp. | Adapted from Nasdaq |
| `nyc_weather_2018.csv` | Long format weather data for New York City across various stations. | The NCEI API's GHCND dataset. |
| `stocks.db` | The `fb_prices` and `aapl_prices` tables contain the stock prices for Facebook and Apple, respectively, for May 20, 2019 through May 24, 2019. Facebook is at a minute granularity, whereas Apple has timestamps that include (fictitious) seconds. | Adapted from Nasdaq |
| `weather_by_station.csv` | Long format weather data for New York City across various stations, along with station information. | The NCEI API's GHCND dataset and the `stations` endpoint. |
| `weather_stations.csv` | Information on all the stations providing weather data for New York City. | The NCEI API's `stations` endpoint. |
| `weather.db` | The `weather` table contains New York City weather data, while the `stations` table contains information on the stations. | The NCEI API's GHCND dataset and the `stations` endpoint. |

### Sources
- The Nasdaq data contains stock data by the minute and was collected before Nasdaq updated their website. The old site will be shut down soon, but while it is still active, the data can be found here: [FB](https://old.nasdaq.com/symbol/fb/interactive-chart), [AAPL](https://old.nasdaq.com/symbol/aapl/interactive-chart). Note that the Apple data was collected prior to the [August 2020 stock split](https://www.marketwatch.com/story/3-things-to-know-about-apples-stock-split-2020-08-28). Additional data can be found on the new [Nasdaq website](https://www.nasdaq.com/market-activity/stocks). 
- The National Centers for Environmental Information (NCEI) provides an [API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2), which we use to access the [*Global Historical Climatology Network - Daily* (GHCND) dataset](https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf).
- The [`stock_analysis`](https://github.com/stefmolin/stock-analysis) package contains easy to use interfaces for basic technical analysis of stocks. We will walk through the construction of this package in *Chapter 7, Financial Analysis &ndash; Bitcoin and the Stock Market*.