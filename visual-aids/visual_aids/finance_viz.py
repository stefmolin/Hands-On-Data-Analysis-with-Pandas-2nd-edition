"""Functions for creating visual aids for finance concepts."""

import random
import string

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import stock_analysis


RED = '#B30000'
GREEN = '#5BC95B'
BLUE = '#00B3B3'


def support_and_resistance():
    """Show sample support and resistance for Netflix stock in 2018"""

    reader = stock_analysis.StockReader('2018-01-01', '2018-12-31')

    # get Netflix data
    nflx = reader.get_ticker_data('NFLX')

    # plot the evolution of closing price over time
    ax = stock_analysis.StockVisualizer(nflx).evolution_over_time(
        'close', figsize=(15, 3), legend=False, color=BLUE,
        title='Understanding support and resistance'
    )

    ref_lines = [
        (315, 0.55, 0.77, GREEN, 'support (buy now)'),
        (250, 0.12, 0.17, GREEN, ''),
        (280, 0.25, 0.3, GREEN, ''),
        (280, 0.78, 0.83, GREEN, ''),
        (260, 0.85, 0.92, GREEN, ''),
        (230, 0.93, 0.96, GREEN, ''),
        (385, 0.46, 0.53, GREEN, ''),
        (420, 0.43, 0.55, RED, 'resistance (sell now)'),
        (285, 0.05, 0.16, RED, ''),
        (335, 0.17, 0.38, RED, ''),
        (385, 0.6, 0.77, RED, ''),
        (330, 0.8, 0.83, RED, ''),
        (290, 0.86, 0.96, RED, '')
    ]

    for y, xmin, xmax, color, label in ref_lines:
        ax.axhline(y, xmin, xmax, color=color, label=label)

    arrows = [
        ('2018-08-26', 315, 0, 20, GREEN),
        ('2018-02-17', 250, 0, 10, GREEN),
        ('2018-04-02', 290, 0, 20, GREEN),
        ('2018-11-03', 280, 0, 10, GREEN),
        ('2018-12-01', 260, 0, 10, GREEN),
        ('2018-12-29', 230, 0, 10, GREEN),
        ('2018-06-10', 385, 0, 20, GREEN),
        ('2018-07-20', 420, 0, -20, RED),
        ('2018-02-04', 285, 0, -10, RED),
        ('2018-03-02', 335, 0, -10, RED),
        ('2018-04-27', 335, 0, -10, RED),
        ('2018-10-10', 385, 0, -10, RED),
        ('2018-11-12', 330, 0, -10, RED),
        ('2018-12-20', 290, 0, -10, RED)
    ]

    for date, y, growx, growy, color in arrows:
        ax.arrow(date, y, growx, growy, width=2, alpha=0.5, color=color)

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    ax.set_xlabel('')
    ax.set_ylabel('price')
    ax.yaxis.set_major_formatter(FormatStrFormatter('$%1.0f'))
    ax.legend(bbox_to_anchor=(0.72, -0.25), ncol=3, framealpha=0)
    
    return ax


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

        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    real_stock = f'real stock is at location {string.ascii_uppercase[stock_location]}'
    
    return real_stock, axes