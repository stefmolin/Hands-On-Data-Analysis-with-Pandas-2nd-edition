# About the data

| File | Description | Source |
| --- | --- | --- |
| `earthquakes.csv` | Earthquake data from September 18, 2018 through October 13, 2018. |  The US Geological Survey (USGS) earthquake API. |
| `example_data.csv` | Five rows from `earthquakes.csv` containing a subset of the columns. |  The US Geological Survey (USGS) earthquake API. |
| `parsed.csv` | Data from `earthquakes.csv` with an additional column for the location (parsed from the data to handle multiple names for the same entity). |  The US Geological Survey (USGS) earthquake API. |
| `quakes.db` | A SQLite database of a single table, `tsunamis`, which contains all data on the earthquakes in `earthquakes.csv` that were accompanied by a tsunami. |  The US Geological Survey (USGS) earthquake API. |
| `tsunamis.csv` | Data for all earthquakes in `earthquakes.csv` that were accompanied by a tsunami. |  The US Geological Survey (USGS) earthquake API. |

### Source
Information on the US Geological Survey (USGS) earthquake API can be found [here](https://earthquake.usgs.gov/fdsnws/event/1/). In this chapter, we walk through collecting this data.
