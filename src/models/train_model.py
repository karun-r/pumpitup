import pandas as pd
from scipy import stats

def chi_squared_test(df, col_x, col_y, p_threshold):
    contingency_tmp = pd.crosstab(df[col_y],df[col_x])
    #(contingency_tmp)
    chi2, p, dof, expected = stats.chi2_contingency(contingency_tmp.values)
    if p <= p_threshold:
        print("Correlated. Has a p-value of ",p)
        #contingency_tmp
    else:
        print("Not Correlated. Has a p-value of  ",p)