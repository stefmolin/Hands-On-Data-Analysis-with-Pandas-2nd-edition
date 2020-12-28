"""Script for merging the logs in a month-by-month simulation."""

import os
import sys
import pandas as pd

def cat_csvs(format_string_file_pattern, index_col, month_list):
    """
    Utility function for concatentating CSV files from simulation.

    Parameters:
        - format_string_file_pattern: The pattern for the file name with `{}` in the place of the month
        - index_col: The column with the datetimes to sort on.
        - month_list: The list of the months as formatted in the file names.

    Returns:
        A concatenated `pandas.DataFrame`
    """
    return pd.concat([
        pd.read_csv(
            format_string_file_pattern.format(file), index_col=index_col, parse_dates=True
        ) for file in month_list
    ]).sort_index()

def get_spillover(data, when):
    """Returns data from spillover"""
    try:
        return data.loc[when]
    except KeyError:
        return pd.DataFrame()

if __name__ == '__main__':
    # make sure we write the files to the proper directory no matter where we called the script from
    directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(directory)

    logs_2018 = cat_csvs(
        'logs/{}_2018.csv', 'datetime',
        ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    )
    logs_2018.loc['2018'].to_csv('logs/logs_2018.csv') # sometimes the simulation overshoots the end date

    logs_2019 = pd.concat([cat_csvs('logs/{}_2019.csv', 'datetime', ['jan', 'feb', 'mar']), get_spillover(logs_2018, '2019')]).sort_index()
    logs_2019.loc['2019-Q1'].to_csv('logs/logs_2019.csv') # sometimes the simulation overshoots the end date

    hackers_2018 = cat_csvs(
        'logs/hackers_{}_2018.csv', 'start',
        ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    )
    hackers_2018.loc['2018'].to_csv('logs/hackers_2018.csv')

    hackers_2019 = pd.concat([
        cat_csvs('logs/hackers_{}_2019.csv', 'start', ['jan', 'feb', 'mar']), get_spillover(hackers_2018, '2019')
    ]).sort_index()
    hackers_2019.loc['2019-Q1'].to_csv('logs/hackers_2019.csv')

    print('All done!')
