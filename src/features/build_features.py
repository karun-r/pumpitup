import pandas as pd
import math
#import os
#print(os.getcwd())
#from src.data import make_dataset

def get_age_from_year(df, year_col_name):
    if not (isinstance(df, pd.core.frame.DataFrame)):
        type_rec = type(df)
        error_msg = str.format("Type Exception occured. Expecting a dataframe. Received {0}", type_rec)
        raise TypeError()
    if year_col_name not in df:
        error_msg = str.format("{0} column doesn't exist in the dataframe", year_col_name)
        raise KeyError(error_msg)
    col_dtype = df[year_col_name].dtype
    if col_dtype != 'int64':
        error_msg = str.format("{0} column is not of the expected datatype (int). It is {1}", year_col_name, col_dtype)
        raise TypeError("error_msg")
    most_recent_year = df[year_col_name].max()
    #Subtract the construction year from the most recent year to get the age of the pump
    df['age'] =  most_recent_year - df[year_col_name]
    #As we had records about pump for which the construction year is mentioned as 0, it is possible that for some pumps, age = most_recent_year.
    #We need to replace them with the average age of the other pumps.
    #Other choices - try to predict the age based on other factors.
    tmp_list = df.loc[df['age'] != most_recent_year,]['age'].tolist()  #Store the ages
    mean_val = math.floor(sum(tmp_list)/len(tmp_list)) #Compute mean
    df.loc[df['age'] == most_recent_year,'age'] = mean_val #Mean Imputation
    return df