"""Visual aids for machine learning concepts."""

import pkg_resources

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import auc


def confusion_matrix():
    """Create a visual aid for understanding the confusion matrix."""

    ax = sns.heatmap(
        np.array([[1, 0], [0, 1]]), cbar=False, cmap=ListedColormap(['whitesmoke', 'lightgray']),
        annot=np.array([
            ['TP\n(True Positive)', 'FP\n(False Positive)'], 
            ['FN\n(False Negative)', 'TN\n(True Negative)']
        ]), fmt="", annot_kws={'size': 15, 'weight': 'bold'}
    )
    ax.set_xticklabels([True, False])
    ax.set_xlabel('Actual', fontsize=18)
    ax.set_yticklabels([True, False], rotation=0)
    ax.set_ylabel('Predicted', fontsize=18)
    ax.set_title('Confusion Matrix', fontsize=25)

    return ax


def portion_of_confusion_matrix_considered(metrics):
    """Show the portion of the confusion matrix considered for a pair of metrics."""
    if not isinstance(metrics, set):
        metrics = set(metrics)

    if metrics == {'precision', 'recall'}:
        data = [
            ['precision + recall', 'precision'], 
            ['recall', 'not considered']
        ]
    elif metrics == {'sensitivity', 'specificity'}:
        data = [
        ['sensitivity', 'specificity'], 
        ['sensitivity', 'specificity']
    ]
    else:
        raise ValueError(f'Not sure how to deal with metrics "{metrics}"')

    ax = sns.heatmap(
        np.array([[0.5, 1], [1, 0]]), cbar=False, cmap=ListedColormap(['white', 'lightgray', 'whitesmoke']),
        annot=np.array(data), fmt='', annot_kws={'size': 12, 'weight': 'bold'}, linewidths=0.3, linecolor='black'
    )
    ax.set_xticklabels([True, False])
    ax.set_xlabel('Actual', fontsize=12)
    ax.set_yticklabels([True, False], rotation=0)
    ax.set_ylabel('Predicted', fontsize=12)
    ax.set_title('Portion of Confusion Matrix Considered', fontsize=16)
    
    plt.tight_layout()

    return ax


def logistic_sigmoid():
    """Show the logistic sigmoid plot"""
    x = np.linspace(-10, 10)
    y = 1. / (1. + np.exp(-x))
    fig = plt.plot(x, y)[0].figure
    plt.title('Logistic Sigmoid Function')
    plt.xlabel('x')
    plt.ylabel('y')
    return fig.axes


def roc_curve():
    """Show example ROC curves."""
    data = pd.read_csv(pkg_resources.resource_stream(__name__, 'data/sample_roc_curves.csv'))

    ax = sns.lineplot(
        data=data, hue='label', x='x', y='y', palette='Greens'
    )

    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)

    # formatting 
    ax.set_title('Sample ROC Curves')
    ax.set_xlabel('False Positive Rate (FPR)')
    ax.set_ylabel('True Positive Rate (TPR)')

    handles, labels = ax.get_legend_handles_labels()
    for i, label in enumerate(labels):
        curve_data = data.query(f'label == "{label}"')
        labels[i] = f'{label}; AUC is {auc(curve_data.x, curve_data.y):.2}'
    ax.legend(handles=handles, labels=labels)

    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    
    return ax


def isolation_forest():
    """Show an example of a single tree in an isolation forest."""
    df = pd.DataFrame({
        'feature_1': [0, 1, 2, 8, 3.5, 2, 3], 
        'feature_2': [1, 2, 1.5, 0.25, 0.73, 1, 2]
    })

    fig = plt.figure(figsize=(20, 30))
    grid_dims = (6, 8)
    axes = []

    # original data
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='starting data', 
        ax=plt.subplot2grid(grid_dims, (0, 4), colspan=2)
    )
    axes.append(ax)
    plt.subplots_adjust(hspace=0.25)

    # first split
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='randomly split using feature_1', 
        ax=plt.subplot2grid(grid_dims, (1, 4), colspan=2)
    )
    ax.axvline(x=4, label='first split', color='red')
    ax.annotate(
        'pick random value of x\nfrom range of feature 1\n(which is [0,8])', 
        xy=(4, 1), xytext=(4.15, 1.25), arrowprops=dict(arrowstyle='->')
    )
    ax.legend()
    axes.append(ax)

    # second split
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='continue splitting', 
        ax=plt.subplot2grid(grid_dims, (2, 2), colspan=2)
    )
    ax.axvline(x=4, label='prior split', color='black')
    ax.axvline(x=1.25, label='new split', color='red')
    ax.legend()
    ax.annotate(
        'pick random value of x\nfrom range of feature 1\nin subsection (i.e. [0,4])', 
        xy=(1.24, 2.8), xytext=(-1.75, 3.8), arrowprops=dict(arrowstyle='->')
    )
    ax.annotate('', xy=(6.6, 3), xytext=(9.25, 4.2), arrowprops=dict(arrowstyle='->'))
    axes.append(ax)

    # third split
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='focus on left section', 
        ax=plt.subplot2grid(grid_dims, (3, 0), colspan=2)
    )
    ax.axvline(x=4, label='prior splits', color='black')
    ax.axvline(x=1.25, color='black')
    ax.axhline(y=1.79, xmax=0.1875, label='new split', color='red')
    ax.annotate(
        'pick random\nvalue from range\nof feature 2\n([0.25,2])', 
        xy=(0.75, 1.79), xytext=(-4, 2.3), arrowprops=dict(arrowstyle='->')
    )
    ax.legend()
    ax.annotate(' path\nlength\n  = 3', xy=(0, 1), xytext=(-0.25, 0.25), arrowprops=dict(arrowstyle='->'))
    ax.annotate(' path\nlength\n  = 3', xy=(1, 2), xytext=(-0.25, 2.55), arrowprops=dict(arrowstyle='->'))
    ax.annotate('', xy=(6.6, 3), xytext=(9.25, 4.2), arrowprops=dict(arrowstyle='->'))
    axes.append(ax)

    # fourth split
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='focus on middle section', 
        ax=plt.subplot2grid(grid_dims, (3, 4), colspan=2)
    )
    ax.axvline(x=4, label='prior splits', color='black')
    ax.axvline(x=1.25, color='black')
    ax.axvline(x=2.45, label='new split', color='red')
    ax.annotate('', xy=(1, 3), xytext=(-1.2, 4), arrowprops=dict(arrowstyle='->'))
    ax.legend()
    axes.append(ax)

    # fifth split
    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='final split', 
        ax=plt.subplot2grid(grid_dims, (4, 3), colspan=2)
    )
    ax.axvline(x=4, label='prior splits', color='black')
    ax.axvline(x=1.25, color='black')
    ax.axvline(x=2.45, color='black')
    ax.axhline(y=1.4, xmin=0.1875, xmax=0.32, label='new split', color='red')
    ax.legend()
    ax.annotate(' path\nlength\n  = 4', xy=(2, 1.5), xytext=(1.35, 1.65), arrowprops=dict(arrowstyle='->'))
    ax.annotate(' path\nlength\n  = 4', xy=(2, 1), xytext=(1.35, 0.3), arrowprops=dict(arrowstyle='->'))
    ax.annotate('', xy=(1.5, 3), xytext=(4.42, 4.1), arrowprops=dict(arrowstyle='->'))
    axes.append(ax)

    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='final split', 
        ax=plt.subplot2grid(grid_dims, (4, 5), colspan=2)
    )
    ax.axvline(x=4, label='prior splits', color='black')
    ax.axvline(x=1.25, color='black')
    ax.axvline(x=2.45, color='black')
    ax.axhline(y=0.85, xmin=0.325, xmax=0.5, label='new split', color='red')
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.legend()
    ax.annotate(' path\nlength\n  = 4', xy=(3, 2), xytext=(2.75, 2.25), arrowprops=dict(arrowstyle='->'))
    ax.annotate(' path\nlength\n  = 4', xy=(3.5, 0.73), xytext=(2.75, 0.1), arrowprops=dict(arrowstyle='->'))
    ax.annotate('', xy=(7, 3), xytext=(3.6, 4), arrowprops=dict(arrowstyle='->'))
    axes.append(ax)

    ax = df.plot(
        x='feature_1', y='feature_2', kind='scatter', title='point isolated', 
        ax=plt.subplot2grid(grid_dims, (2, 6), colspan=2)
    )
    ax.axvline(x=4, label='prior split', color='black')
    ax.legend()
    ax.annotate('path length = 1', xy=(8, 0.25), xytext=(5.5, 0.5), arrowprops=dict(arrowstyle='->'))
    ax.annotate('', xy=(2, 3), xytext=(-1.2, 4), arrowprops=dict(arrowstyle='->'))
    axes.append(ax)

    for ax in axes:
        ax.set_ylim(0, 3)

    return axes

def bias_variance_tradeoff():
    """Create subplots to illustrate the bias-variance tradeoff"""
    np.random.seed(5)
    x = np.linspace(start=-1, stop=0.25, num=20)
    y = x**2 + np.random.uniform(-0.25, 0.25, size=20)

    fig, axes = plt.subplots(1, 3, figsize=(15, 3))

    for ax in axes:
        ax.plot(x, y, 'bo')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_ylim(-0.4, 1.2)

    axes[0].plot(x, y, 'r-')
    axes[0].set_title('high variance (overfitting)')

    axes[1].plot(x, x * -1 - 0.1, 'r-')
    axes[1].set_title('high bias (underfitting)')

    axes[2].plot(x, x**2, 'r-')
    axes[2].set_title('balance')

    return axes
