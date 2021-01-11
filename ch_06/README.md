# Chapter 6: Plotting with Seaborn and Customization Techniques

This chapter continues the discussion on data visualization by teaching you how to use the `seaborn` library for visualizing your long form data and giving you the tools you need to customize your visualizations, making them presentation-ready.

## Content

There are three notebooks that we will work through, each numbered according to when they will be used:

- [`1-introduction_to_seaborn.ipynb`](./1-introduction_to_seaborn.ipynb): introduces you to plotting with `seaborn`
- [`2-formatting_plots.ipynb`](./2-formatting_plots.ipynb): covers formatting and labeling plots
- [`3-customizing_visualizations.ipynb`](./3-customizing_visualizations.ipynb): provides some exposure to plot customizations including reference lines, annotations, and custom colormaps

-----

There is also a **bonus** notebook that walks through an example of plotting data on a map using COVID-19 cases worldwide: [`covid19_cases_map.ipynb`](./covid19_cases_map.ipynb). It can be used to get started with maps in Python and also builds upon some of the formatting discussed in the chapter.

-----

In addition, we have two Python modules that contain functions that we will use in the aforementioned notebooks:

- [`color_utils.py`](./color_utils.py): includes various functions for working with colors in Python
- [`viz.py`](./viz.py): contains one function for generating regression and residuals plots for each pair of variables in the dataset using `seaborn` and another function for generating a KDE with reference lines for 1, 2, and 3 standard deviations from the mean

All the datasets necessary for the aforementioned notebooks, along with information on them, can be found in the [`data/`](./data) directory. The end-of-chapter exercises will use these datasets as well; solutions to the exercises can be found in the repository's [`solutions/ch_06/`](../solutions/ch_06) directory.

