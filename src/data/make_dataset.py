# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import os
import pickle as pk
import sys 

sys.path.insert(0, os.getcwd())


from src.features.build_features import get_age_from_year

logger = logging.getLogger(__name__)

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

