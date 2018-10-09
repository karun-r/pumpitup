# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import os
import pickle as pk
import sys 
import configparser
import ast

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from pandas.util.testing import assert_frame_equal

sys.path.insert(0, os.getcwd())

from src.features.build_features import get_age_from_year

from src.visualization.visualize import ValidationError


config = configparser.ConfigParser()
config.read('src/config.ini')


logger = logging.getLogger(__name__)
logging.basicConfig(filename='src/logfile.log',level=logging.INFO)

def merge(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info('merging raw files to create a consolidated copy')
    training_data_temp = pd.read_csv("data/raw/trainingdata.csv")
    training_labels_temp = pd.read_csv("data/raw/traininglabels.csv")
    training_data = pd.merge(training_data_temp,training_labels_temp, on="id",how="inner")
    return(training_data)

def save_data(artifact, file_path, is_data_frame = True):
    if is_data_frame:
        msg = str.format("saving the dataset to the folder at {0}", file_path)
        if not (isinstance(artifact, pd.core.frame.DataFrame) ):
            raise TypeError("save_interim_data() argument must be a dataframe if is_data_frame is set to True")
        else:
            logger.info(msg)
            artifact.to_csv(file_path, index= False)
    else:
        with open(file_path, "wb") as data_file:
            pk.dump(artifact, data_file, pk.HIGHEST_PROTOCOL)

def scale_dataset(df):
    """
        Scales the int/float columns using the MinMax scaler. Uses the SCALABLE_FEATURES key from the config file.
        Throws an error if the key is empty.
    """

    scalable_features = ast.literal_eval(config['DATA_PREP']['SCALABLE_FEATURES'])
    if scalable_features is None:
        raise KeyError("key not found in config file for scalable features")
    scaler = MinMaxScaler()
    try:
        df[scalable_features] = scaler.fit_transform(df[scalable_features])
        is_scaling_success = True
    except:
        raise ValidationError("Problem with scaling dataset",scalable_features)
    
    for col in scalable_features:
        if df[col].max() == 1 and df[col].min() == 0:
            is_scaling_success = True
        else:
            is_scaling_success = False
    if is_scaling_success:
        logger.info("scaling completed succesfully")
    else:
        logger.info("error after scaling")
    return df
    
def get_dummy_features(df):
    """
        Takes in the feed from the config file that has the list of categorical columns and generates dummy columns for them.
        Throws an error if the key is empty.
    """
    dummy_features = ast.literal_eval(config['DATA_PREP']['dummy_features'])
    if dummy_features is None:
        raise KeyError("key not found in config file for dummy features")
    ret_df = pd.get_dummies(df,columns = [col for col in dummy_features])
    return ret_df

def process_incoming_data(df):
    """
        Takes in dataset as the input and performs the below steps:
            1. Check if it has the same schema as raw dataset. Throws an error if it doesn't have the required columns. Takes only
               the required columns in case if it has more.
            2. Drops the columns that are not being in use by the model. Uses the config file to fetch.
            3. Performs the necessary steps like scaling and creating dummy features. 
    """
    if not isinstance(df,pd.core.frame.DataFrame):
        raise TypeError("Incoming data not a dataframe.")
    training_data_temp = pd.read_csv("data/raw/trainingdata.csv")
    if df.columns.all() != training_data_temp.columns.all():
        raise KeyError("Columns doesnt match with the initial raw data")
    appended_data = training_data_temp.append(df, ignore_index = True )
    merged_data_age = get_age_from_year(appended_data,"construction_year")
    req_columns = pd.read_csv("data/interim/merged_data.csv").columns
    req_columns = [col for col in req_columns if col != 'status_group']
    reduced_data = merged_data_age[req_columns]
    scaled_dataset = scale_dataset(reduced_data)
    excluded_features = ast.literal_eval(config['DATA_PREP']['exclude_features'])
    scaled_dataset.drop([col for col in excluded_features], axis = 1, inplace = True)
    dummy_dataset = get_dummy_features(scaled_dataset)
    test_dataset = dummy_dataset.tail(df.shape[0])
    return test_dataset

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    raw_path = "data/raw"
    interim_path = "data/interim"
    external_path = "data/external"
    processed_path = "data/processed"
    merged_data = merge(raw_path,processed_path)
    #starting point for new data points that need prediction
    #TODO move to a diff place for easier access
    test_data = pd.read_csv("data/raw/testdata.csv")
    prep_data = process_incoming_data(test_data)
    training_data_by_model =  pd.read_csv("data/processed/X_train.csv")
    assert_frame_equal(prep_data.head(10), training_data_by_model.head(10))
    merged_data_age = get_age_from_year(merged_data, "construction_year")
    save_data(merged_data , "data/interim/merged_data.csv")
    scaled_dataset = scale_dataset(merged_data_age)
    excluded_features = ast.literal_eval(config['DATA_PREP']['exclude_features'])
    scaled_dataset.drop([col for col in excluded_features], axis = 1, inplace = True)
    dummy_dataset = get_dummy_features(scaled_dataset)
    y = dummy_dataset['status_group']
    X = dummy_dataset.drop('status_group',axis = 1, inplace = False)
    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.33, random_state=89)
    save_data(X_train, "data/processed/X_train.csv")
    save_data(X_test, "data/processed/X_test.csv")
    save_data(y_train.to_frame(), "data/processed/y_train.csv")
    save_data(y_test.to_frame(), "data/processed/y_test.csv")

