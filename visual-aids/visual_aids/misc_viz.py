"""Miscellaneous visual aids"""

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


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
    plt.ylim(-1.25, 1.25)
    plt.legend()

    # remove axes
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)

    # remove box around image
    for spine in axes.spines:
        axes.spines[spine].set_visible(False)

    return axes
