import pandas as pd 

def check_data(df): 
    print('shape: ' +  str(df.shape))
    res = pd.concat([df.isna().sum().rename('null'),
                     df.nunique().rename('unique'),
                     pd.Series(len(df) - df.nunique()).rename('duplicate'),
                     df.iloc[0].rename('data_example'),
                     df.dtypes.rename('data_type')],
                     axis=1
                   )
    return res