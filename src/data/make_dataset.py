# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
import os

def merge(input_filepath, output_filepath,for_eda = False):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    training_data_temp = pd.read_csv("data/raw/trainingdata.csv")
    training_labels_temp = pd.read_csv("data/raw/traininglabels.csv")
    training_data = pd.merge(training_data_temp,training_labels_temp, on="id",how="inner")
    if for_eda:
        return training_data
    else:
        training_data.to_csv("data/processed/training.csv", index = False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    raw_path = "data/raw"
    interim_path = "data/interim"
    external_path = "data/external"
    processed_path = "data/processed"
    merge(raw_path,processed_path)
