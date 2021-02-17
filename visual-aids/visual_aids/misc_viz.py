"""Miscellaneous visual aids"""

import pkg_resources

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans


def low_med_high_bins_viz(data, column, ylabel, title, figsize=(15, 3)):
    """Visualize the low, medium, and high equal-width bins."""
    ax = data.plot(y=column, figsize=figsize, color='black', title=title)

    xlims = ax.get_xlim()

    for bin_name, hatch, bounds in zip(
        ['low', 'med', 'high'],
        ['///', '', '\\\\\\'],
        pd.cut(data[column], bins=3).unique().categories.values
    ):
        plt.axhspan(bounds.left, bounds.right, alpha=0.2, label=bin_name, hatch=hatch, color='black')
        plt.annotate(f'  {bin_name}', xy=(xlims[0], (bounds.left + bounds.right) / 2.1), ha='left')

    ax.set(xlabel='', ylabel=ylabel)
    plt.legend(bbox_to_anchor=(1, 0.75), frameon=False)

    return ax


def quartile_bins_viz(data, column, ylabel, title, figsize=(15, 8)):
    """Visualize quartile bins."""
    ax = data.plot(y=column, figsize=figsize, color='black', title=title)

    xlims = ax.get_xlim()

    for bin_name, hatch, bounds in zip(
        [r'$Q_1$', r'$Q_2$', r'$Q_3$', r'$Q_4$'],
        ['\\\\\\', '', '///', '||||'],
        pd.qcut(data.volume, q=4).unique().categories.values
    ):
        plt.axhspan(bounds.left, bounds.right, alpha=0.2, label=bin_name, hatch=hatch, color='black')
        plt.annotate(f'  {bin_name}', xy=(xlims[0], (bounds.left + bounds.right) / 2.1), fontsize=11)

    ax.set(xlabel='', ylabel=ylabel)
    plt.legend(bbox_to_anchor=(1, 0.67), frameon=False, fontsize=14)

    return ax


def resampling_example():
    """Shows before and after resampling data at the minute level to the daily level."""
    np.random.seed(0)

    index = pd.date_range('2018-01-01', freq='T', periods=365*24*60)
    raw = pd.DataFrame(
        np.random.uniform(0, 10, size=index.shape[0]), index=index
    )

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    raw.plot(legend=False, ax=axes[0], title='raw data')
    raw.resample('1D').sum().plot(legend=False, ax=axes[1], title='daily totals')

    for ax in axes:
        ax.set_xlabel('date')
        ax.set_ylabel('events')

    plt.suptitle('Raw vs. Resampled Data')
    
    return axes


def elliptical_orbit():
    """Draw an example of a planet with an elliptical orbit around its star."""
    fig, axes = plt.subplots(1, 1)

    orbit = Ellipse(xy=(0, 0), width=2, height=1.5, facecolor='lightblue')
    axes.add_artist(orbit)

    axes.plot([-1, 0], [0, 0])

    axes.annotate(
        'semi-major axis', 
        xy=(-0.5, 0), 
        xytext=(-0.8, -0.2), 
        arrowprops=dict(arrowstyle='wedge')
    )
    axes.annotate(
        'orbit center', 
        xy=(0, 0), 
        xytext=(-0.21, 0.115), 
        arrowprops=dict(arrowstyle='wedge')
    )

    plt.plot(
        [-.75], [0.5], 
        marker='o', markersize=4, 
        color='green', label='planet'
    )
    plt.plot(
        [0], [0], 
        marker='o', markersize=10, 
        color='orange', label='star'
    )

    # formatting
    plt.xlim(-1.25, 1.25)
    plt.ylim(-1.1, 0.75)
    plt.legend(loc='lower center', ncol=2)

    # remove axes
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)

    # remove box around image
    for spine in axes.spines:
        axes.spines[spine].set_visible(False)

    return axes


def market_segmentation_cluster_example():
    """Show an example of market segmentation clusters."""
    df = pd.read_csv(pkg_resources.resource_stream(__name__, 'data/market_segmentation_cluster_example.csv'))

    model = KMeans(3, random_state=2).fit(df)
    ax = sns.scatterplot(
        x=df.products_viewed, 
        y=df.products_purchased, 
        hue=model.labels_, 
        palette=sns.color_palette('colorblind', n_colors=3)
    )

    plt.legend(title='group')
    plt.title('Clustering for Market Segmentation')
    plt.xlabel('products viewed')
    plt.ylabel('products purchased')

    return ax