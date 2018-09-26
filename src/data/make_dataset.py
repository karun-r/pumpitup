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

def save_interim_data(artifact, file_path, is_data_frame = True):
    if is_data_frame:
        msg = str.format("saving the dataset to interim folder at {0}", file_path)
        if not (isinstance(artifact, pd.core.frame.DataFrame) ):
            raise TypeError("save_interim_data() argument must be a dataframe if is_data_frame is set to True")
        else:
            logger.info(msg)
            artifact.to_csv(file_path)
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


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    raw_path = "data/raw"
    interim_path = "data/interim"
    external_path = "data/external"
    processed_path = "data/processed"
    merged_data = merge(raw_path,processed_path)
    merged_data_age = get_age_from_year(merged_data, "construction_year")
    save_interim_data(merged_data , "data/interim/merged_data.csv")
    scaled_dataset = scale_dataset(merged_data_age)
    excluded_features = ast.literal_eval(config['DATA_PREP']['exclude_features'])
    scaled_dataset.drop([col for col in excluded_features], axis = 1, inplace = True)
    dummy_dataset = get_dummy_features(scaled_dataset)
    print(dummy_dataset.shape)