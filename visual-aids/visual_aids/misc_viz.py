"""Miscellaneous visual aids"""

import pkg_resources

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans


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
    plt.ylim(-0.75, 1.25)
    plt.legend()

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