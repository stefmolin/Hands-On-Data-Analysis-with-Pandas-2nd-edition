# Chapter 11: Machine Learning Anomaly Detection

This chapter revisits anomaly detection on login attempt data, using machine learning techniques, all while giving you a taste of how the workflow looks in practice.

## Content

We will work through five notebooks emulating a real-world scenario using the simulated data in the `logs/` directory. Here's a breakdown of the files included in this chapter:

- [`logs/`](./logs): Directory containing all simulated log files for the analysis
- [`user_data/`](./user_data): Directory containing information on the user base used for the simulation (for the `simulate.py` script to use)
- [`0-simulating_the_data.ipynb`](./0-simulating_the_data.ipynb): Jupyter notebook showing how data was simulated
- [`1-EDA_unlabeled_data.ipynb`](./1-EDA_unlabeled_data.ipynb): Jupyter notebook used to perform our EDA of the unlabeled data
- [`2-unsupervised_anomaly_detection.ipynb`](./2-unsupervised_anomaly_detection.ipynb): Jupyter notebook used to test out some unsupervised anomaly detection alogrithms
- [`3-EDA_labeled_data.ipynb`](./3-EDA_labeled_data.ipynb): Jupyter notebook used to perform our EDA of the labeled data
- [`4-supervised_anomaly_detection.ipynb`](./4-supervised_anomaly_detection.ipynb): Jupyter notebook used to build and evaluate supervised anomaly detection models
- [`5-online_learning.ipynb`](./5-online_learning.ipynb): Jupyter notebook used to implement an online learning classifier
- [`merge_logs.py`](./merge_logs.py): Python script for merging the logs of individually simulated months
- [`run_simulations.sh`](./run_simulations.sh): Bash script for simulating and merging the log files (this is used to generate the data)
- [`simulate.py`](./simulate.py): Python script for simulating the data using the [`login_attempt_simulator` package](https://github.com/stefmolin/login-attempt-simulator)


The end-of-chapter exercises will use the data in the [`logs/`](./logs) directory to explore additional algorithms for machine learning anomaly detection; solutions to these exercises can be found in the repository's [`solutions/ch_11/`](../solutions/ch_11) directory.

