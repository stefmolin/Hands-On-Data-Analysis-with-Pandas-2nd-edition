import pandas as pd

def cat_csvs(format_string_file_pattern, index_col, month_list):
    """
    Utility function for concatentating CSV files from simulation.

    Parameters:
        - format_string_file_pattern: The pattern for the file name with `{}` in the place of the month
        - index_col: The column with the datetimes to sort on.
        - month_list: The list of the months as formatted in the file names.

    Returns:
        A concatenated pandas DataFrame
    """
    return pd.concat([
        pd.read_csv(
            format_string_file_pattern.format(file), index_col=index_col, parse_dates=True
        ) for file in month_list
    ])

if __name__ == '__main__':
    logs_2018 = cat_csvs(
        'logs/{}_2018.csv', 'datetime', 
        ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    )
    logs_2018['2018'].sort_index().to_csv('logs/logs_2018.csv') # sometimes the simulation overshoots the end date

    logs_2019 = pd.concat([cat_csvs('logs/{}_2019.csv', 'datetime', ['jan', 'feb', 'mar']), logs_2018.get('2019')])
    logs_2019['2019-Q1'].to_csv('logs/logs_2019.csv') # sometimes the simulation overshoots the end date

    hackers_2018 = cat_csvs(
        'logs/hackers_{}_2018.csv', 'start',
        ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    )
    hackers_2018['2018'].sort_index().to_csv('logs/hackers_2018.csv')

    hackers_2019 = pd.concat([
        cat_csvs('logs/hackers_{}_2019.csv', 'start', ['jan', 'feb', 'mar']), hackers_2018.get('2019')
    ])
    hackers_2019['2019-Q1'].sort_index().to_csv('logs/hackers_2019.csv')

    print('All done!')
