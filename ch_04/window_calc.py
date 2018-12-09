def window_calc(df, func, agg_dict, *args, **kwargs):
    """
    Run a window calculation of your choice on a DataFrame.
    
    Parameters:
        - df: The DataFrame to run the calculation on.
        - func: The window calculation method that takes df 
                as the first argument.
        - agg_dict: Information to pass to `agg()`, could be a 
                    dictionary mapping the columns to the aggregation 
                    function to use, a string name for the function, 
                    or the function itself.
        - args: Positional arguments to pass to `func`.
        - kwargs: Keyword arguments to pass to `func`.
    
    Returns:
        - A new DataFrame object.
    """
    return df.pipe(func, *args, **kwargs).agg(agg_dict)