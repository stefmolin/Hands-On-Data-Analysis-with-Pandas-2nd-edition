import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

def elbow_point(
    data, pipeline, kmeans_step_name='kmeans', k_range=range(1, 11)
):
    """Graph the elbow point to find the optimal k for clustering"""
    scores = []
    for k in k_range:
        pipeline.named_steps[kmeans_step_name].n_clusters = k
        pipeline.fit(data)
        scores.append(pipeline.score(data) * -1)

    fig = plt.figure()
    plt.plot(k_range, scores, 'bo-')
    plt.xlabel('k')
    plt.ylabel('value of data on objective function')
    plt.suptitle('Elbow Point Plot')
    plt.close()

    return fig

def plot_residuals(y_test, preds):
    """
    Plot residuals to evaluate regression.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y

    Returns:
        Subplots of residual scatter plot and 
        residual KDE plot.
    """
    residuals = y_test - preds

    fig, axes = plt.subplots(1, 2, figsize=(15, 3))
    axes[0].scatter(np.arange(residuals.shape[0]), residuals)
    residuals.plot(kind='kde', ax=axes[1])
    plt.suptitle('Residuals')
    return axes

def plot_roc(y_test, preds):
    """
    Plot ROC curve to evaluate classification.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y

    Returns:
        Plotted ROC curve.
    """
    fpr, tpr, thresholds = roc_curve(y_test, preds)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')
    plt.plot(fpr, tpr, color='red', lw=2, label='model')
    plt.legend(loc='lower right')
    plt.title('ROC curve')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.annotate(f'AUC: {roc_auc_score(y_test, preds):.2}', xy=(.43, .025))

def confusion_matrix_visual(y_true, y_pred, class_labels, **kwargs):
    """
    Create a confusion matrix heatmap to evaluate classification.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y
        - class_labels: What to label the classes.
        - kwargs: Additional keyword arguments for `seaborn.heatmap()`

    Returns:
        A confusion matrix heatmap.
    """
    mat = confusion_matrix(y_true, y_pred)
    ax = sns.heatmap(
        mat.T, square=True, annot=True, fmt='d', 
        cbar=True, cmap=plt.cm.Blues, **kwargs
    )
    plt.xlabel('Actual')
    plt.ylabel('Model Prediction')
    tick_marks = np.arange(len(class_labels)) + 0.5
    plt.xticks(tick_marks, class_labels)
    plt.yticks(tick_marks, class_labels, rotation=0)
    plt.title('Confusion Matrix')
    return ax

def plot_multi_class_roc(y_test, preds):
    """
    Plot ROC curve to evaluate classification.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y

    Returns:
        ROC curve.
    """
    data = pd.DataFrame({'actual' : y_test, 'predicted': preds})
    fig, ax = plt.subplots(1, 1)
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')
    class_labels = np.sort(y_test.unique())
    for class_label in class_labels:
        class_data = data.apply(lambda x: np.where(x == class_label, 1, 0))
        fpr, tpr, thresholds = roc_curve(class_data.actual, class_data.predicted)
        auc = roc_auc_score(class_data.actual, class_data.predicted)
        ax.plot(fpr, tpr, lw=2, label=f"""class {class_label}; AUC: {auc:.2}""")
    plt.legend()
    plt.title('Multi-class ROC curve')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')

def pca_scatter(X, labels, cbar_label, color_map='brg'):
    """
    Create a 2D scatter plot from 2 PCA components of X

    Parameters:
        - X: The X data for PCA
        - labels: The y values
        - cbar_label: The label for the colorbar
        - color_map: Name of the color_map to use. Default is 'brg'

    Returns:
        Matplotlib Axes object
    """
    pca = Pipeline([('scale', MinMaxScaler()), ('pca', PCA(2, random_state=0))]).fit(X)
    data = pca.transform(X)
    ax = plt.scatter(
        data[:, 0], data[:, 1],
        c=labels, edgecolor='none', alpha=0.5,
        cmap=plt.cm.get_cmap(color_map, 2)
    )
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    cbar = plt.colorbar()
    cbar.set_label(cbar_label)
    cbar.set_ticks([0, 1])
    plt.legend(
        ['explained variance\n'
        'comp. 1: {:.3}\ncomp. 2: {:.3}'.format(
            *pca.named_steps['pca'].explained_variance_ratio_
        )]
    )
    return ax
    
def pca_scatter_3d(X, labels, cbar_label, color_map='brg', elev=10, azim=15):
    """
    Create a 3D scatter plot from 3 PCA components of X
    
    Parameters:
        - X: The X data for PCA
        - labels: The y values
        - cbar_label: The label for the colorbar
        - color_map: Name of the color_map to use. Default is 'brg'
        - elev: The degrees of elevation to view the graph from. Default is 10.
        - azim: The azimuth angle on the xy plane (rotation around the z-axis). Default is 15.
    
    Returns:
        Matplotlib Axes object
    """
    pca = Pipeline([('scale', MinMaxScaler()), ('pca', PCA(3, random_state=0))]).fit(X)
    data = pca.transform(X)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    p = ax.scatter3D(
        data[:, 0], data[:, 1], data[:, 2], alpha=0.5,
        c=labels, cmap=plt.cm.get_cmap(color_map, 2)
    )
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('component 1')
    ax.set_ylabel('component 2')
    ax.set_zlabel('component 3')
    cbar = fig.colorbar(p)
    cbar.set_ticks([0, 1])
    cbar.set_label(cbar_label)
    plt.legend(
        ['explained variance\n'
        'comp. 1: {:.3}\ncomp. 2: {:.3}\ncomp. 3: {:.3}'.format(
            *pca.named_steps['pca'].explained_variance_ratio_
        )]
    )
    return ax
