import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import bernoulli, binom, expon, poisson, norm, skewnorm
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
from statsmodels.tsa.seasonal import seasonal_decompose

def _non_symmetric_data():
    """Generate non-symmetric data for plots"""
    # generate data
    np.random.seed(0)
    return pd.Series(
        np.random.gamma(7, 5, size=1000) * np.random.choice([-2.2, -1.85, 0, -0.4, 1.33], size=1000), name='x'
    )

def anscombes_quartet():
    """Plot Anscombe's Quartet along with summary statistics."""

    # get data
    anscombe = sns.load_dataset('anscombe').groupby('dataset')

    # define subplots and titles
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()
    titles = ['linear', 'non-linear', 'linear with outlier', 'vertical with outlier']

    for ax, (group_name, group_data), title in zip(axes, anscombe, titles):
        # get x, y
        x, y = group_data.x, group_data.y

        # make a scatter plot
        ax.scatter(x, y)

        # add title and labels
        ax.set_title(f'{group_name} - {title}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # align the axes limits
        ax.set_xlim((3, 19.5))
        ax.set_ylim((2, 13))

        # plot the regression line
        m, b = np.polyfit(x, y, 1)
        reg_x = np.append([0, 20], x)
        reg_y = [m*num + b for num in reg_x]
        ax.plot(reg_x, reg_y, 'r--')

        # annotate the summary statistics
        ax.annotate(
            f"""ρ = {np.corrcoef(x,y)[0][1]:.2}\ny = {m:.2}x + {b:.2}\n\n{
                r'$μ_x$'
            } = {np.mean(x):2} | {
                r'$σ_x$'
            } = {np.std(x):.2}\n{
                r'$μ_y$'
            } = {np.mean(y):.2} | {r'$σ_y$'} = {np.std(y):.2}""", xy=(13, 2.5)
        )

    # give the plots a title
    plt.suptitle("Anscombe's Quartet", fontsize=16, y=0.95)

    return axes

def cdf_example():
    """Subplots to understand CDF."""
    data = _non_symmetric_data()
    ecdf = ECDF(data)

    fig, axes = plt.subplots(1, 3, figsize=(15, 3))

    for ax in axes:
        ax.plot(ecdf.x, ecdf.y)
        ax.set_xlabel('x')
        ax.set_ylabel('F(x)')

    # less than or equal to 50
    axes[0].fill_between(ecdf.x[ecdf.x <= 50], ecdf.y[ecdf.x <= 50], 0, alpha=0.5)
    axes[0].axhline(0.93, xmax=0.76, linestyle='dashed')
    axes[0].set_title(r'$P(X \leq 50) \approx 93\%$')

    # equal to 50
    axes[1].fill_between(ecdf.x[ecdf.x == 50], ecdf.y[ecdf.x == 50], 0, alpha=0.5)
    axes[1].set_title(r'$P(X = 50) = 0\%$')

    # greater than 50
    axes[2].fill_between(ecdf.x[ecdf.x >= 50], ecdf.y[ecdf.x >= 50], 0, alpha=0.5)
    axes[2].axhline(0.93, xmax=0.76, linestyle='dashed')
    axes[2].set_title(r'$P(X > 50) = 1 - P(X \leq 50) \approx 7\%$')
    
    plt.suptitle('Understanding the CDF', y=1.1)
    
    return axes

def common_dists():
    """Show some commonly used distributions."""
    # prep the subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    # gaussian
    mu, sigma = 0, 1
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    axes[0].plot(x, norm.pdf(x, mu, sigma))
    axes[0].set_title('Gaussian PDF')
    axes[0].set_ylabel('density')
    axes[0].set_xlabel('x')
    axes[0].annotate(r'$\mu$', xy=(mu, 0.4), xytext=(mu - 0.09, 0.3), arrowprops=dict(arrowstyle='->'))
    axes[0].annotate(
        '', xy=(mu - sigma, 0.25), xytext=(mu + sigma, 0.25),
        arrowprops=dict(arrowstyle='|-|, widthB=0.5, widthA=0.5')
    )
    axes[0].annotate(r'$2\sigma$', xy=(mu - 0.15, 0.22))

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

    # exponential
    x = np.linspace(0, 5, 100)
    axes[2].plot(x, expon.pdf(x, scale=1/3))
    axes[2].set_title('Exponential PDF')
    axes[2].set_ylabel('density')
    axes[2].set_xlabel('x')
    axes[2].annotate(r'$\lambda$ = 3', xy=(0, 3), xytext=(0.5, 2.8), arrowprops=dict(arrowstyle='->'))
    
    # Bernoulli of coin toss
    axes[3].bar(['heads', 'tails'], bernoulli.pmf([0, 1], p=0.5))
    axes[3].set_title('Bernoulli with fair coin toss (p = 0.5)')
    axes[3].set_ylabel('probability')
    axes[3].set_xlabel('coin toss result')
    axes[3].set_ylim(0, 1)
    
    # Binomial of tossing a fair coin many times
    x = np.arange(0, 10)
    axes[4].plot(x, binom.pmf(x, n=x.shape, p=0.5), linestyle='--', marker='o')
    axes[4].set_title('Binomial PMF - many Bernoulli trials')
    axes[4].set_ylabel('probability')
    axes[4].set_xlabel('number of heads')

    # Poisson PMF (probability mass function) because this is a discrete random variable
    x = np.arange(0, 10)
    axes[5].plot(x, poisson.pmf(x, mu=3), linestyle='--', marker='o')
    axes[5].set_title('Poisson PMF')
    axes[5].set_ylabel('mass')
    axes[5].set_xlabel('x')
    axes[5].annotate(r'$\lambda$ = 3', xy=(3, 0.225), xytext=(1.9, 0.2), arrowprops=dict(arrowstyle='->'))

    # add a title
    plt.suptitle('Some commonly used distributions', fontsize=15, y=0.95)
    
    return axes

def correlation_coefficient_examples():
    """Show some examples of scatter plots with correlation coefficients."""
    # starting data
    np.random.seed(0)
    x = np.random.normal(size=100)
    y = np.random.normal(size=100)

    # make subplots
    fig, axes = plt.subplots(1, 4, figsize=(16, 3))
    
    # no correlation
    axes[0].scatter(x, y)
    axes[0].set_title(f'ρ = {np.round(np.corrcoef(x, y)[0][1], 2)}')
    
    # weak negative correlation
    a, b = x, (x + y*2)*-1
    axes[1].scatter(a, b)
    axes[1].set_title(f'ρ = {np.round(np.corrcoef(a, b)[0][1], 2)}')
    
    # strong positive correlation
    s, t = x, (x - np.random.uniform(1, 3, size=100))
    axes[2].scatter(s, t)
    axes[2].set_title(f'ρ = {np.round(np.corrcoef(s, t)[0][1], 2)}')
    
    # perfect negative correlation
    c, d = x, (x - y*.1) * -1
    axes[3].scatter(c, d)
    axes[3].set_title(f'ρ = {np.round(np.corrcoef(c, d)[0][1], 2)}')
    
    for ax in axes:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    return axes

def different_modal_plots():
    """Show unimodal, bimodal, and multimodal example distributions."""

    # distribution details
    x = np.linspace(-4, 4, 500)
    loc1, scale1, size1 = (-2, 0.75, 150)
    loc2, scale2, size2 = (3, 0.5, 50)
    loc3, scale3, size3 = (0.4, 1, 150)

    # make subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 3))

    # plot unimodal
    axes[0].plot(x, norm.pdf(x))

    # plot bimodal
    bimodal_pdf = norm.pdf(x, loc=loc1, scale=scale1) * float(size1) / (size1 + size2) + \
       norm.pdf(x, loc=loc2, scale=scale2) * float(size2) / (size1 + size2)
    axes[1].plot(x, bimodal_pdf)

    # plot multimodal
    multimodal_pdf = bimodal_pdf + norm.pdf(x, loc=loc3, scale=scale3) * float(size3) / (size1 + size2)
    axes[2].plot(x, multimodal_pdf)

    # label everything and format
    for ax, title in zip(axes, ['unimodal', 'bimodal', 'multimodal']):
        ax.set_ylim(0, 0.45)
        ax.set_xlabel('x')
        ax.set_ylabel('density')
        ax.set_title(title)

    return axes

def effect_of_std_dev():
    """Display two normal distributions with different standard deviations."""
    np.random.seed(0)
    data = pd.DataFrame({
        'σ = 0.5': np.random.normal(scale=0.5, size=1000),
        'σ = 2': np.random.normal(scale=2, size=1000)
    })

    ax = data.plot(kind='density', title='Different Population Standard Deviations', figsize=(5, 2))
    plt.xlabel('x')

    return ax

def example_boxplot():
    """Generate an example box plot."""
    non_symmetric = _non_symmetric_data()

    # find the quartiles and iqr
    q1_y, median_y, q3_y = non_symmetric.quantile([0.25, 0.5, 0.75])
    iqr = q3_y - q1_y

    # make the boxplot
    ax = non_symmetric.plot(kind='box', figsize=(6, 6), title='Box plot')

    # label the box
    ax.annotate('median', xy=(0.945, median_y + 2))
    ax.annotate(r'$Q_3$', xy=(1, q3_y), xytext=(1.08, q3_y - 5))
    ax.annotate(r'$Q_1$', xy=(1, q1_y), xytext=(1.08, q1_y))
    ax.annotate(
        'IQR', xy=(0.9, (q3_y + q1_y)/2), xytext=(0.8, (q3_y + q1_y)/2 - 2.85),
        arrowprops=dict(arrowstyle='-[, widthB=3.3, lengthB=0.5')
    )

    # label the whiskers
    ax.annotate(r'$Q_3 + 1.5 * IQR$', xy=(1.05, q3_y + 1.5 * iqr - 7))
    ax.annotate(r'$Q_1 - 1.5 * IQR$', xy=(1.05, q1_y - 1.5 * iqr - 2))

    # label the outliers
    ax.annotate(
        'outlier', xy=(0.99, non_symmetric.min()), xytext=(0.8, non_symmetric.min() - 2.1),
        arrowprops=dict(arrowstyle='->')
    )

    for i, val in enumerate(non_symmetric[non_symmetric > q3_y + 1.5*iqr]):
        if not i: 
            text = 'outliers' 
            x, y = 0.75, 102
        else:
            text = '' 
            x, y = 0.87, 103
        ax.annotate(
            text, xy=(0.99, val), xytext=(x, y),
            arrowprops=dict(facecolor='black', arrowstyle='-|>')
        )

    return ax

def example_histogram():
    """Generate an example histogram."""
    non_symmetric = _non_symmetric_data()

    # get the bins
    bins = np.histogram_bin_edges(non_symmetric)

    # plot the data
    ax = non_symmetric.plot(
        kind='hist', legend=False, figsize=(15, 3),
        title=f'Histogram with 10 bins (each of width {bins[1] - bins[0]:.2f})'
    )
    ax.set_xlabel('x')

    # annotate measures of central tendency
    x_mode, x_mean, x_median = non_symmetric.mode(), non_symmetric.mean(), non_symmetric.median()
    ax.annotate(
        f'mode ({x_mode.iat[0]:.0f})', xy=(x_mode, 210), xytext=(x_mode + 5, 250), arrowprops=dict(arrowstyle='->')
    )
    ax.annotate(
        f'mean ({x_mean:.0f})', xy=(x_mean, 180), xytext=(x_mean - 20, 220), arrowprops=dict(arrowstyle='->')
    )
    ax.annotate(
        f'median ({x_median:.0f})', xy=(x_median, 180), xytext=(x_median - 12, 280), arrowprops=dict(arrowstyle='->')
    )
    plt.ylim((0, 320))

    return ax

def example_kde():
    """Generate an example KDE."""
    non_symmetric = _non_symmetric_data()

    # plot the data
    ax = non_symmetric.plot(
        kind='kde', legend=False, figsize=(15, 3), 
        title='Kernel density estimate', bw_method=0.1, ylim=(0, 0.02)
    )
    ax.set_xlabel('x')

    # find measures of central tendency
    x_mode, x_mean, x_median = non_symmetric.mode(), non_symmetric.mean(), non_symmetric.median()

    # mark measures of central tendency with vertical dashed lines
    ax.axvline(x_mean, ymax=0.2, color='orange', linestyle='dashed')
    ax.axvline(x_median, ymax=0.5, color='orange', linestyle='dashed')
    ax.axvline(x_mode.iat[0], ymax=0.87, color='orange', linestyle='dashed')

    # annotate measures of central tendency
    ax.annotate('mode', xy=(x_mode - 11, 0.0178))
    ax.annotate('mean', xy=(x_mean, 0.0015), xytext=(x_mean - 70, 0.001), arrowprops=dict(arrowstyle='->'))
    ax.annotate('median', xy=(x_median, 0.01), xytext=(x_median - 50, 0.013), arrowprops=dict(arrowstyle='->'))

    return ax

def example_regression():
    """Show example regression."""
    # generate data
    np.random.seed(0)
    ice_cream_sales = pd.DataFrame({
        'temps': np.linspace(20, 40, num=30),
        'sales': np.abs(np.append(np.arange(2, 22), np.arange(22, 32)) + np.random.randint(-10, 10, size=30))
    })
    
    # make the scatter plot
    ax = ice_cream_sales.plot(
        kind='scatter', x='temps', y='sales', xlim=(15, 45), ylim=(0, 40), figsize=(12, 5),
        title='Using regression to predict ice cream sales'
    )

    # plot regression line
    m, b = np.polyfit(ice_cream_sales.temps, ice_cream_sales.sales, 1)
    reg_x = ice_cream_sales.temps
    reg_y = [m*num + b for num in reg_x]
    ax.plot(reg_x, reg_y, 'r-', label='regression line')
    
    # note the equation of the regression line
    ax.annotate(f'y = {m:.2f}x + {b:.2f}', xy=(15.5, 32))

    # extend the line to show extrapolation
    ax.plot([-b/m, 20], [0, 20*m + b], 'r:', label='extrapolated regression line')
    ax.plot([40, 45], [m*x + b for x in [40, 45]], 'r:')

    # labeling
    plt.legend()
    plt.xlabel('temperature in °C')
    plt.ylabel('ice cream sales')
    
    return ax

def example_scatter_plot():
    """Show example scatter plot."""
    # generate data
    np.random.seed(0)
    ice_cream_sales = pd.DataFrame({
        'temps': np.linspace(20, 40, num=30),
        'sales': np.abs(np.append(np.arange(2, 22), np.arange(22, 32)) + np.random.randint(-10, 10, size=30))
    })
    
    # make the scatter plot
    ax = ice_cream_sales.plot(
        kind='scatter', x='temps', y='sales', xlim=(15, 45), ylim=(0, 40), figsize=(12, 5),
        title='ice cream sales at a given temperature'
    )

    # labeling
    plt.xlabel('temperature in °C')
    plt.ylabel('ice cream sales')
    
    return ax

def hist_and_kde():
    """Show histogram with KDE."""
    # get data
    data = _non_symmetric_data()

    # plot histogram and KDE
    ax = data.plot(kind='hist', density=True, bins=12, alpha=0.5, title='Estimating the distribution', figsize=(15, 3))
    data.plot(kind='kde', ax=ax, color='blue').set_xlabel('x')

    return ax

def non_linear_relationships():
    """Plot logarithmic and exponential data along with correlation coefficients."""
    # make subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 3))

    # plot logarithmic
    log_x = np.linspace(0.01, 10)
    log_y = np.log(log_x)
    axes[0].scatter(log_x, log_y)
    axes[0].set_title(f'ρ = {np.round(np.corrcoef(log_x, log_y)[0][1], 2):.2f}')

    # plot exponential
    exp_x = np.linspace(0, 10)
    exp_y = np.exp(exp_x)
    axes[1].scatter(exp_x, exp_y)
    axes[1].set_title(f'ρ = {np.round(np.corrcoef(exp_x, exp_y)[0][1], 2):.2f}')

    # labels
    for ax in axes:
        ax.set_xlabel('x')
        ax.set_ylabel('y')

    return axes

def skew_examples():
    """Visualize left, right, and no skew distributions."""

    # create subplots
    fig, ax = plt.subplots(1, 3, figsize=(20, 4))

    # determine skew
    a = 4

    # find stats for annotation
    mean_skew_val = skewnorm.mean(a)
    median_skew_val = skewnorm.median(a)

    # get x data where PDF has value
    x = np.linspace(skewnorm.ppf(0.001, a), skewnorm.ppf(0.999, a), 100)

    # plot left skew
    ax[0].plot(x * -1, skewnorm.pdf(x, a))
    ax[0].set_title('Left/Negative Skewed')

    # annotate left skew's mode
    ax[0].axvline(-0.42, 0.72, 0.925, color='orange')
    ax[0].text(s='mode', x=-0.49, y=0.5, rotation=90)
    ax[0].axvline(-0.42, 0, 0.53, color='orange')

    # annotate left skew's median
    ax[0].axvline(median_skew_val * -1, 0.52, 0.83, color='orange')
    ax[0].text(s='median', x=-0.74, y=0.35, rotation=90)
    ax[0].axvline(median_skew_val * -1, 0, 0.3, color='orange')

    # annotate left skew's mean
    ax[0].axvline(mean_skew_val * -1, 0.26, 0.77, color='orange')
    ax[0].text(s='mean', x=-0.84, y=0.16, rotation=90)
    ax[0].axvline(mean_skew_val * -1, 0, 0.09, color='orange')

    # plot no skew normal
    ax[1].plot(x, norm.pdf(x, loc=x.mean(), scale=0.56))
    ax[1].set_title('No Skew')

    # annotate mean, median, and mode
    ax[1].text(s='  mean\nmedian\n  mode', x=x.mean() - 0.25, y=0.25)
    ax[1].axvline(x.mean(), 0.5, 0.94, color='orange')
    ax[1].axvline(x.mean(), 0, 0.3, color='orange')

    # plot right skew
    ax[2].plot(x, skewnorm.pdf(x, a))
    ax[2].set_title('Right/Positive Skewed')

    # annotate right skew's mode
    ax[2].axvline(0.42, 0.72, 0.925, color='orange')
    ax[2].text(s='mode', x=0.35, y=0.5, rotation=90)
    ax[2].axvline(0.42, 0, 0.53, color='orange')

    # annotate right skew's median
    ax[2].axvline(median_skew_val, 0.52, 0.83, color='orange')
    ax[2].text(s='median', x=0.6, y=0.35, rotation=90)
    ax[2].axvline(median_skew_val, 0, 0.3, color='orange')

    # annotate right skew's mean
    ax[2].axvline(mean_skew_val, 0.26, 0.77, color='orange')
    ax[2].text(s='mean', x=0.72, y=0.16, rotation=90)
    ax[2].axvline(mean_skew_val, 0, 0.09, color='orange')

    # label axes and set y-axis limits
    for axes in ax:
        axes.set_xlabel('x')
        axes.set_ylabel('f(x)')
        axes.set_ylim(0, 0.75)

    return ax
    
def time_series_decomposition_example():
    """Show an example of time series decomposition."""
    # generate a random time series
    np.random.seed(0)
    ts = pd.DataFrame({'timestamp' : pd.date_range('2018-01-01', periods=365, freq='D')})
    for i, drift, seasonality, noise in zip(
        ts.index, 
        np.linspace(0, 1, num=365), 
        itertools.cycle(np.append(np.linspace(0, np.pi, num=25), np.linspace(np.pi, 0, num=25, endpoint=False))),
        np.random.uniform(-10, 10, size=365)
    ):
        if i in [0]:
            ts.loc[i, 'value'] = i
        else:
            ts.loc[i, 'value'] = ts.loc[i - 1, 'value'] + drift + np.sin(seasonality) + noise

    # plot the result
    plt.rcParams['figure.figsize'] = [10, 6]
    result = seasonal_decompose(ts.set_index('timestamp').value, freq=50)
    plot = result.plot()
    plt.suptitle('Time Series Decomposition', y=1)
    plt.rcdefaults()