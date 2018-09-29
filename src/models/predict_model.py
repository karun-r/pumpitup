import pickle
import configparser
import os 

import pandas as pd
from sklearn.metrics import accuracy_score

config = configparser.ConfigParser()
config.read('src/config.ini')

X_test  = pd.read_csv("data/processed/X_test.csv")
y_test  = pd.read_csv("data/processed/y_test.csv")

def load_model():
    """
        Loads model from the file system using pickle.
    """
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
        y_predict = clf.predict(x_predict)
        return y_predict
    else:
        y_test  = clf.predict(x_predict)
        accuracy = accuracy_score(y_predict, y_test)
        return accuracy

X_test  = pd.read_csv("data/processed/X_test.csv")
y_test  = pd.read_csv("data/processed/y_test.csv")

model = load_model()

accuracy = predict(model, X_test,y_test)
print(accuracy)
