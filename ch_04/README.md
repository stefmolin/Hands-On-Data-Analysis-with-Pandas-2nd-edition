# Chapter 4: Aggregating Pandas DataFrames

This chapter teaches you how to query and merge `DataFrame` objects, perform complex operations on them, including rolling calculations and aggregations, and how to work effectively with time series data.

## Content

There are four notebooks that we will work through, each numbered according to when they will be used:

- [`1-querying_and_merging.ipynb`](./1-querying_and_merging.ipynb): showcases how to query and merge `DataFrame` objects
- [`2-dataframe_operations.ipynb`](./2-dataframe_operations.ipynb): walks through a variety of data enrichment operations, such as binning and window calculations, and how to perform them efficiently with the `apply()` and `pipe()` methods 
- [`3-aggregations.ipynb`](./3-aggregations.ipynb): discusses how to perform aggregations on the data, including pivot tables, crosstabs, and calculations based on group membership with the `groupby()` method
- [`4-time_series.ipynb`](./4-time_series.ipynb): illustrates how to work effectively with time series

-----

There is also a **bonus** notebook that uses interactive widgets to give you a better understanding of window calculations: [`understanding_window_calculations.ipynb`](./understanding_window_calculations.ipynb).

-----

In addition to the aforementioned notebooks, we have two additional files:
- [`0-weather_data_collection.ipynb`](./0-weather_data_collection.ipynb): (optional) contains the code used to collect the weather data used in the chapter
- [`window_calc.py`](./window_calc.py): contains a function that uses pipes to perform a variety of window calculations

All the datasets necessary for the aforementioned notebooks, along with information on them, can be found in the [`data/`](./data) directory. The end-of-chapter exercises will use the datasets in the [`exercises/`](./exercises) directory; solutions to these exercises can be found in the repository's [`solutions/ch_04/`](../solutions/ch_04) directory.

