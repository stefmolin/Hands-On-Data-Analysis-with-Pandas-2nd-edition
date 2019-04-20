import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score, roc_curve, roc_auc_score, confusion_matrix
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

def adjusted_r2(model, X, y):
	"""
    Calculate the adjusted R^2.

    Parameters:
        - model: Estimator object with a `predict()` method
        - X: The values to use for prediction.
        - y: The true values for scoring.

    Returns:
        The adjusted R^2 score.
    """
	r2 = r2_score(y, model.predict(X))
	n_obs, n_regressors = X.shape
	adj_r2 = 1 - (1 - r2) * (n_obs - 1)/(n_obs - n_regressors - 1)
	return adj_r2

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

def confusion_matrix_visual(y_true, y_pred, class_labels, ax=None, title=None, **kwargs):
    """
    Create a confusion matrix heatmap to evaluate classification.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y
        - class_labels: What to label the classes.
        - ax: The matplotlib Axes object to plot on.
        - title: The title for the confusion matrix
        - kwargs: Additional keyword arguments for `seaborn.heatmap()`

    Returns:
        A confusion matrix heatmap.
    """
    mat = confusion_matrix(y_true, y_pred)
    axes = sns.heatmap(
        mat.T, square=True, annot=True, fmt='d', 
        cbar=True, cmap=plt.cm.Blues, ax=ax, **kwargs
    )
    axes.set_xlabel('Actual')
    axes.set_ylabel('Model Prediction')
    tick_marks = np.arange(len(class_labels)) + 0.5
    axes.set_xticks(tick_marks)
    axes.set_xticklabels(class_labels)
    axes.set_yticks(tick_marks)
    axes.set_yticklabels(class_labels, rotation=0)
    axes.set_title(title or 'Confusion Matrix')
    return axes

def find_threshold(y_test, y_preds, fpr_below, tpr_above):
    """
    Find the threshold to use with `predict_proba()` for classification
    based on the maximum acceptable FPR and the minimum acceptable TPR.
    
    Parameters:
        - y_test: The actual labels.
        - y_preds: The predicted labels.
        - fpr_below: The maximum acceptable FPR.
        - tpr_above: The minimum acceptable TPR.
        
    Returns:
        The thresholds were the criteria are met.
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_preds)
    return thresholds[(fpr <= fpr_below) & (tpr >= tpr_above)]

def plot_roc(y_test, preds, ax=None):
    """
    Plot ROC curve to evaluate classification.

    Parameters: 
        - y_test: The true values for y
        - preds: The predicted values for y as probabilities
        - ax: The Axes to plot on

    Returns:
        Plotted ROC curve.
    """
    if not ax:
        fig, ax = plt.subplots(1, 1)
    fpr, tpr, thresholds = roc_curve(y_test, preds)
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')
    ax.plot(fpr, tpr, color='red', lw=2, label='model')
    ax.legend(loc='lower right')
    ax.set_title('ROC curve')
    ax.set_xlabel('False Positive Rate (FPR)')
    ax.set_ylabel('True Positive Rate (TPR)')
    ax.annotate(f'AUC: {roc_auc_score(y_test, preds):.2}', xy=(.43, .025))

def plot_multi_class_roc(y_test, preds, ax=None):
    """
    Plot ROC curve to evaluate classification.

    Parameters:
        - y_test: The true values for y
        - preds: The predicted values for y as probabilities
        - ax: The Axes to plot on

    Returns:
        ROC curve.
    """
    if not ax:
        fig, ax = plt.subplots(1, 1)
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')
    class_labels = np.sort(y_test.unique())
    for i, class_label in enumerate(class_labels):
        actuals = np.where(y_test == class_label, 1, 0)
        predicted_probabilities = preds[:,i]
        fpr, tpr, thresholds = roc_curve(actuals, predicted_probabilities)
        auc = roc_auc_score(actuals, predicted_probabilities)
        ax.plot(fpr, tpr, lw=2, label=f"""class {class_label}; AUC: {auc:.2}""")
    ax.legend()
    ax.set_title('Multi-class ROC curve')
    ax.set_xlabel('False Positive Rate (FPR)')
    ax.set_ylabel('True Positive Rate (TPR)')

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

class PartialFitPipeline(Pipeline):
    """Subclass of sklearn.pipeline.Pipeline that supports the `partial_fit()` method."""

    def partial_fit(self, X, y):
        """Run `partial_fit()` for online learning estimators when used in a pipeline."""
        for _, step in self.steps[:-1]:
            X = step.fit_transform(X)
        self.steps[-1][1].partial_fit(X, y)
        return self