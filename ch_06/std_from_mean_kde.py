import itertools

def std_from_mean_kde(data):
    """
    Plot the KDE of the pandas series along with vertical
    reference lines for each standard deviation from the mean.
    
    Parameters:
        - data: pandas Series with numeric data
    
    Returns:
        Matplotlib Axes object.
    """
    mean_mag, std_mean = data.mean(), data.std()
    
    ax = data.plot(kind='kde')
    ax.axvline(mean_mag, color='b', alpha=0.2, label='mean')
    
    colors = ['green', 'orange', 'red']
    multipliers = [1, 2, 3]
    signs = ['-', '+']
    
    for sign, (color, multiplier) in itertools.product(
        signs, zip(colors, multipliers)
    ):
        adjustment = multiplier * std_mean
        if sign == '-':
            value = mean_mag - adjustment
            label = '{} {}{}{}'.format(
                r'$\mu$',
                r'$\pm$',
                multiplier,
                r'$\sigma$'
            )
        else:
            value = mean_mag + adjustment
            label = None
        ax.axvline(value, color=color, label=label, alpha=0.5)
    
    ax.legend()
    return ax