import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

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