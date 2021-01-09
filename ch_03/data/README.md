# About the data

| File | Description | Source |
| --- | --- | --- |
| `bitcoin.csv` | Daily opening, high, low, and closing price of bitcoin, along with volume traded and market capitalization for 2017 through 2018. | CoinMarketCap |
| `dirty_data.csv` | 2018 weather data for New York City, manipulated to introduce data issues. | Modified version of the data from the NCEI API's GHCND dataset. |
| `long_data.csv` | Long format temperature data for New York City in October 2018 from the Boonton 1 station, containing daily temperature at time of observation, minimum temperature, and maximum temperature. | The NCEI API's GHCND dataset |
| `nyc_temperatures.csv` | Temperature data for New York City in October 2018 measured from LaGuardia airport, containing daily minimum, maximum, and average temperature. | The NCEI API's GHCND dataset |
| `sp500.csv` | Daily opening, high, low, and closing price of the S&P 500 stock index, along with volume traded and adjusted close for 2017 through 2018. | The `stock_analysis` package (see *Chapter 7, Financial Analysis &ndash; Bitcoin and the Stock Market*). |
| `wide_data.csv` | Wide format temperature data for New York City in October 2018 from the Boonton 1 station, containing daily temperature at time of observation, minimum temperature, and maximum temperature. | The NCEI API's GHCND dataset |

### Sources
- [CoinMarketCap](https://coinmarketcap.com) provides historical price data for a variety of cryptocurrencies. For the first edition, the bitcoin data was collected from CoinMarketCap using the `stock_analysis` package; however, changes to the website led to changing the data source to Yahoo! Finance. The bitcoin data that was collected before the CoinMarketCap website change should be equivalent to the historical data that can be viewed on [this](https://coinmarketcap.com/currencies/bitcoin/historical-data/) page.
- The National Centers for Environmental Information (NCEI) provides an [API](https://www.ncdc.noaa.gov/cdo-web/webservices/v2), which we use to access the [*Global Historical Climatology Network - Daily* (GHCND) dataset](https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf).
- The [`stock_analysis`](https://github.com/stefmolin/stock-analysis) package contains easy to use interfaces for basic technical analysis of stocks. We will walk through the construction of this package in *Chapter 7, Financial Analysis &ndash; Bitcoin and the Stock Market*.
