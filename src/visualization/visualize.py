import pandas as pd
import seaborn as sns
import warnings
import matplotlib.pyplot as plt

class ValidationError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)
        print(errors)

def describe_dataset(df):
    '''
        This will list out each column in the dataset with a brief summary of it's attributes.
        TODO:
            1. Add statistical properties for numeric columns
            2. Include the sample of non zero values for numeric columns
    '''
    if not (isinstance(df, pd.core.frame.DataFrame)):
        raise TypeError("Type exception occured. Expecting a dataframe.")
    df_cols = df.columns
    out_cols = ['name','type','first_five','last_five','unique_values','total_values','na_values']
    out_df = pd.DataFrame(columns = out_cols)
    for col in df_cols:
        out_dict = {}
        out_dict['name'] = col
        out_dict['type'] = df[col].dtype
        out_dict['first_five'] = list(df[col].head())
        out_dict['last_five']  = list(df[col].tail())
        out_dict['unique_values'] = len(df[col].unique())
        out_dict['total_values'] = len(df[col])
        out_dict['na_values'] = (df[col].isna().sum())
        out_df = out_df.append(out_dict, ignore_index =True)
    return out_df


def get_contingency_table(df):
    '''
        Used for visualising relationships between two categorical variables
    '''
    if not (isinstance(df, pd.core.frame.DataFrame)):
        raise TypeError("Type exception occured. Expecting a dataframe.")
    col_df = df.columns
    if (len(col_df) > 2):
        raise ValidationError("Dataframe must have only two columns.",col_df)
    return pd.crosstab(index = df[col_df[0]], columns = df[col_df[1]])


def get_box_plot(df, target_column_index = 1):
    '''
        Used for visualising relationships between a continous variable (independent) and a categorical variable (dependent)
    '''
    if not (isinstance(df, pd.core.frame.DataFrame)):
        raise TypeError("Type exception occured. Expecting a dataframe.")
    col_df = df.columns
    if (len(col_df) > 2):
        raise ValidationError("Dataframe must have only two columns.",col_df)
    if target_column_index == 1:
        x_index,y_index = 1,0
    elif target_column_index == 0:
        x_index,y_index = 0,1
    else:
        raise ValidationError("target_column_index must be set to 0 or 1.",target_column_index)
    sns.boxplot(x=df.columns[x_index], y=df.columns[y_index], data = df)
    plt.show()


def helper_summarize(df, row,target_column, target_column_type):
    '''
        Based on the two columns that we want to see a relationship, this function will determine the appropriate
        visual to use.
    '''
    print("Feature Name: ", row['name'])
    print("Feature Type: ", row['type'])
    print("Sample Data: ",row['first_five'],"......",row['last_five'])
    temp_df = df[[row['name'],target_column]]
    if row['type'] == "object" and target_column_type == "object": #both categorical variables
        print(get_contingency_table(temp_df))
    elif row['type'] in ["int64","float64"] and target_column_type == "object": #continous
        get_box_plot(temp_df)


def summarize_dataset(df,dependent_variable = None):
    '''
        Initial validation and calling the helper_summarize function from here to get the plots/relationships.
        In this function, we also make an assumption on the target variable if nothing is provided by the user.
    '''
    if not (isinstance(df, pd.core.frame.DataFrame)):
        raise TypeError("Type exception occured. Expecting a dataframe.")
    if dependent_variable is None:
        dependent_variable = df.columns[-1]
        warning.warn("As the dependent_variable was not used, we assume that the last column of your dataframe as the dependent variable")
    df_ = describe_dataset(df)
    for idx,row in df_.iterrows():
        if row['name'] != dependent_variable:
            helper_summarize(df, row,dependent_variable,"object")