# Chapter 8: Rule-Based Anomaly Detection

This chapter covers [simulating data](https://github.com/stefmolin/login-attempt-simulator) and applying everything learned in chapters 1-6 to catching hackers attempting to authenticate to a website, using rule-based strategies for anomaly detection.

## Content

After discussing how to build the `login_attempt_simulator` package, we will build the `simulate.py` script for running the simulation. The simulation will generate the files in the `logs/` and `user_data/` directories. Then, we will use the simulated data in the `logs/` directory to conduct our analysis in the `anomaly_detection.ipynb` notebook.

All of the aforementioned files are provided in this directory:

- [`logs/`](./logs): Directory containing all simulated log files for the analysis
- [`user_data/`](./user_data): Directory containing information on the user base used for the simulation (for the `simulate.py` script to use)
- [`anomaly_detection.ipynb`](./anomaly_detection.ipynb): Jupyter notebook used to perform our analysis
- [`simulate.py`](./simulate.py): Python script for simulating the data using the [`login_attempt_simulator` package](https://github.com/stefmolin/login-attempt-simulator)

The end-of-chapter exercises will use the [`simulate.py`](./simulate.py) script to generate a new dataset; solutions to these exercises can be found in the repository's [`solutions/ch_08/`](../solutions/ch_08) directory.

