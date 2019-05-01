import random
import string

import matplotlib.pyplot as plt

def random_walk_stock_comparison(df, choices=[-1, 1], probs=[0.5, 0.5], seed=2):
    """
    Model a random walk from a stock's first closing price in the dataframe.
    Displays 3 random walks and the actual data in randomly assigned subplots.
    Can you find the real data?

    Parameters: 
        - df: The dataframe of the real stock data.
        - choices: The choices of step sizes, defaults to [-1, 1].
        - probs: The probability of getting each step size, 
                 defaults to [0.5, 0.5]. This should be the same 
                 size as choices.
        - seed: The random seed for repeatability.

    Returns:
        Prints the location of the actual data and 
        returns the matplotlib Axes object.        
    """
    random.seed(seed)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    stock_location = random.randint(0, 3)

    for i, ax in enumerate(axes.flatten()):
        if i == stock_location:
            ax.plot(df.index, df.close)
        else:
            steps = random.choices(
                choices, weights=probs, k=len(df.index) - 1
            )
            walk = [df.first('1B').close.iat[0]]
            for step in steps:
                walk.append(walk[-1] + step)
            ax.plot(df.index, walk)
        ax.set_ylabel('price')
        
        ax.set_title(string.ascii_uppercase[i])

    real_stock = f'real stock is at location {string.ascii_uppercase[stock_location]}'
    
    return real_stock, axes