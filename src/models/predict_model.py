import pickle
import configparser
import os 
import logging

import pandas as pd
from sklearn.metrics import accuracy_score

config = configparser.ConfigParser()
config.read('src/config.ini')


logger = logging.getLogger(__name__)
logging.basicConfig(filename='src/logfile.log',level=logging.INFO)


def load_model():
    """
        Loads model from the file system using pickle.
    """
    logger.info("loading the trained model from file system.")
    model_path = config['MODEL']['model_path']
    model_exists = os.path.isfile(model_path)
    if model_exists:
        clf = pickle.load(open(model_path, "rb"))
        return clf
    else:
        raise FileNotFoundError("Model not found. Please train the model first.")

def predict(clf, x_predict, y_predict = None):
    """
        Uses the model loaded from pickle to predict the outcome on the test data point y_test. Returns the outcome
    """
    if y_predict is None:
        """
            It is not a test dataset. Cannot report accuracy
        """
        logger.info("predicting the outcome for the provided dataset")
        y_predict = clf.predict(x_predict)
        logger.info(y_predict)
        return y_predict
    else:
        y_test  = clf.predict(x_predict)
        accuracy = accuracy_score(y_predict, y_test)
        return accuracy

