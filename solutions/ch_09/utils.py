import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import auc, average_precision_score, confusion_matrix, precision_recall_curve, r2_score, roc_curve

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