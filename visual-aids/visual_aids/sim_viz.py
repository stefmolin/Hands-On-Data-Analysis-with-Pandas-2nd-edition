"""Visual aids for simulation."""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def show_distributions():
    """Generate a plot for each of distributions used in the simulation."""

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    fig.delaxes(axes[-2])

    # triangular distribution defined by min (a), max (b) and mode
    a, b, mode = 1.5, 5, 2.75
    peak = 2 / (b - a)# peak of PDF is at 2/(b-a)
    axes[0].plot([a, mode, b], [0, peak, 0])
    axes[0].set_title('Triangular PDF')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('density')
    axes[0].annotate('min', xy=(a, 0), xytext=(a + 1, 0), arrowprops=dict(arrowstyle='->'))
    axes[0].annotate('max', xy=(b, 0), xytext=(b - 1.25, 0), arrowprops=dict(arrowstyle='->'))
    axes[0].annotate('peak', xy=(mode, peak), xytext=(mode - 0.2, peak - 0.2), arrowprops=dict(arrowstyle='->'))

    # uniform distribution defined by min (a) and max (b)
    a, b = 0, 1
    peak = 1 / (b - a)
    axes[1].plot([a, a, b, b], [0, peak, peak, 0])
    axes[1].set_title('Uniform PDF')
    axes[1].set_ylabel('density')
    axes[1].set_xlabel('x')
    axes[1].annotate('min', xy=(a, peak), xytext=(a + 0.2, peak - 0.2), arrowprops=dict(arrowstyle='->'))
    axes[1].annotate('max', xy=(b, peak), xytext=(b - 0.3, peak - 0.2), arrowprops=dict(arrowstyle='->'))
    axes[1].set_ylim(0, 1.5)

    # gaussian
    mu, sigma = 1.01, 0.01
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    axes[2].plot(x, stats.norm.pdf(x, mu, sigma) / 100)
    axes[2].set_title('Gaussian PDF')
    axes[2].set_ylabel('density')
    axes[2].set_xlabel('x')
    axes[2].annotate(r'$\mu$', xy=(mu, 0.4), xytext=(mu - 0.001, 0.3), arrowprops=dict(arrowstyle='->'))
    axes[2].annotate(
        '', xy=(mu-sigma, 0.25), xytext=(mu + 0.01, 0.25),
        arrowprops=dict(arrowstyle='|-|, widthB=0.5, widthA=0.5')
    )
    axes[2].annotate(r'$2\sigma$', xy=(mu - 0.002, 0.22))

    # exponential
    x = np.linspace(0, 5, 100)
    axes[3].plot(x, stats.expon.pdf(x, scale=1/3))
    axes[3].set_title('Exponential PDF')
    axes[3].set_ylabel('density')
    axes[3].set_xlabel('x')
    axes[3].annotate(r'$\lambda$ = 3', xy=(0, 3), xytext=(0.5, 2.8), arrowprops=dict(arrowstyle='->'))

    # Poisson PMF (probability mass function) because this is a discrete random variable
    x = np.arange(0, 10)
    axes[5].plot(x, stats.poisson.pmf(x, mu=3), linestyle='--', marker='o')
    axes[5].set_title('Poisson PMF')
    axes[5].set_ylabel('mass')
    axes[5].set_xlabel('x')
    axes[5].annotate(r'$\lambda$ = 3', xy=(3, 0.225), xytext=(1.9, 0.2), arrowprops=dict(arrowstyle='->'))

    plt.suptitle('Understanding the distributions used for the simulation', fontsize=15, y=0.95)

    return axes