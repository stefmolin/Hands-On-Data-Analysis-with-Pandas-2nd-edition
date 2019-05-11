import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import auc, average_precision_score, confusion_matrix, precision_recall_curve, r2_score, roc_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

def elbow_point(
    data, pipeline, kmeans_step_name='kmeans', k_range=range(1, 11)
):
    """
    Graph the elbow point to find an appropriate k for k-means clustering.

    Parameters:
        - data: The features to use
        - pipeline: The scikit-learn pipeline with KMeans
        - kmeans_step_name: The name of the KMeans step in the pipeline
        - k_range: The values of `k` to try

    Returns:
        A matplotlib Axes object
    """
    scores = []
    for k in k_range:
        pipeline.named_steps[kmeans_step_name].n_clusters = k
        pipeline.fit(data)
        scores.append(pipeline.score(data) * -1)

    fig, axes = plt.subplots()
    axes.plot(k_range, scores, 'bo-')
    axes.set_xlabel('k')
    axes.set_ylabel('inertia')
    axes.set_title('Elbow Point Plot')

    return axes


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
    axes[0].set_xlabel('Observation')
    axes[0].set_ylabel('Residual')

    residuals.plot(kind='kde', ax=axes[1])
    axes[1].set_xlabel('Residual')

    plt.suptitle('Residuals')
    return axes


def plot_roc(y_test, preds):
    """
    Plot ROC curve to evaluate classification.

    Parameters:
        - y_test: The true values for y
        - preds: The predicted values for y as probabilities

    Returns:
        Plotted ROC curve.
    """
    fpr, tpr, thresholds = roc_curve(y_test, preds)

    fig, axes = plt.subplots()

    axes.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')
    axes.plot(fpr, tpr, color='red', lw=2, label='model')

    axes.legend(loc='lower right')
    axes.set_title('ROC curve')
    axes.set_xlabel('False Positive Rate (FPR)')
    axes.set_ylabel('True Positive Rate (TPR)')

    axes.annotate(f'AUC: {auc(fpr, tpr):.2}', xy=(.43, .025))

    return axes

def plot_pr_curve(y_test, preds, positive_class=1):
    """
    Plot precision-recall curve to evaluate classification.

    Parameters:
        - y_test: The true values for y
        - preds: The predicted values for y as probabilities
        - positive_class: The label for the positive class in the data

    Returns:
        Plotted precision-recall curve.
    """
    precision, recall, thresholds = precision_recall_curve(y_test, preds)

    fig, axes = plt.subplots()

    axes.axhline(sum(y_test == positive_class)/len(y_test), color='navy', lw=2, linestyle='--', label='baseline')
    axes.plot(recall, precision, color='red', lw=2, label='model')

    axes.legend()
    axes.set_title(
        'Precision-recall curve\n'
        f""" AP: {average_precision_score(
            y_test, preds, pos_label=positive_class
        ):.2} | """
        f'AUC: {auc(recall, precision):.2}'
    )
    axes.set_xlabel('Recall')
    axes.set_ylabel('Precision')

    axes.set_xlim(-0.05, 1.05)
    axes.set_ylim(-0.05, 1.05)

    return axes

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
        - preds: The predicted values for y as probabilities

    Returns:
        ROC curve.
    """
    fig, ax = plt.subplots(1, 1)

    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='baseline')

    class_labels = np.sort(y_test.unique())
    for i, class_label in enumerate(class_labels):
        actuals = np.where(y_test == class_label, 1, 0)
        predicted_probabilities = preds[:,i]
        fpr, tpr, thresholds = roc_curve(actuals, predicted_probabilities)
        auc = roc_auc_score(actuals, predicted_probabilities)
        ax.plot(fpr, tpr, lw=2, label=f"""class {class_label}; AUC: {auc:.2}""")

    plt.legend()
    plt.title('Multi-class ROC curve')
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    return ax

def plot_multi_class_pr_curve(y_test, preds):
    """
    Plot precision-recall curve to evaluate classification.

    Parameters:
        - y_test: The true values for y
        - preds: The predicted values for y as probabilities

    Returns:
        Plotted precision-recall curve.
    """
    class_labels = np.sort(y_test.unique())

    row_count = np.ceil(len(class_labels) / 3).astype(int)
    fig, axes = plt.subplots(row_count, 3, figsize=(15, row_count*5))
    axes = axes.flatten()

    if len(axes) > len(class_labels):
        for i in range(len(class_labels), len(axes)):
            fig.delaxes(axes[i])

    for i, class_label in enumerate(class_labels):
        axes[i].axhline(sum(y_test == class_label)/len(y_test), color='navy', lw=2, linestyle='--', label='baseline')
        actuals = np.where(y_test == class_label, 1, 0)
        predicted_probabilities = preds[:,i]
        precision, recall, thresholds = precision_recall_curve(actuals, predicted_probabilities)
        auc_score = auc(recall, precision)
        ap_score = average_precision_score(actuals, predicted_probabilities)
        axes[i].plot(recall, precision, lw=2, label=f"""AUC: {auc_score:.2}; AP : {ap_score:.2}""")

        axes[i].legend()
        axes[i].set_title(f'Precision-recall curve: class {class_label}')
        axes[i].set_xlabel('Recall')
        axes[i].set_ylabel('Precision')

        axes[i].set_xlim(-0.05, 1.05)
        axes[i].set_ylim(-0.05, 1.05)

    return axes

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
