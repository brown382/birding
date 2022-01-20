import pandas as pd

def read_data(f,date_and_time_column_name='date_and_time',date_and_time_column_positions=[11,12],idf=True,kdc=True):
    '''Read in dataset, combining date and time columns
    Args:
        f (str): file name of dataset
        date_and_time_column_name (str): name of resultant column by combining date and time columns
            default = 'date_and_time'
        date_and_time_column_positions (list of int): location of date and time columns in dataset
            default = [11,12]
        idf (bool): infer_datetime_format option (default = True)
        kdc (bool): keep_date_col option (default = True)
    
    Returns:
        DataFrame: pandas dataframe of dataset'''

    df = pd.read_csv(f,parse_dates={date_and_time_column_name:date_and_time_column_positions},infer_datetime_format=idf,keep_date_col=kdc)
    return df

def keep_columns(df,cols):
    '''Choose which columns from original dataset to keep
    Args:
        df (DataFrame): original dataframe containing all columns
        cols (str or list of str): column names to keep
    
    Returns:
        DataFrame: dataframe with only desired columns'''

    if isinstance(cols,str):
        cols = [cols]
    return df[cols].copy()

def rename_and_lcase_columns(df,rename_dict,lower_case=True):
    '''Rename columns and make all lowercase
    Args:
        df (DataFrame): original dataframe containing original column names
        rename_dict (dictionary): dictionary of columns to rename
        lower_case (bool): whether or not to make all columns lowercase (default = True)
        
    Returns:
        DataFrame: dataframe with renamed columns and all in lowercase'''

    df.rename(columns=rename_dict,inplace=True)

    if lower_case:
        df.columns = [x.lower() for x in df.columns]

    return df

def focus_on_year(df,y):
    '''Filter dataframe for a specific year, using the date column
    Args:
        df (DataFrame): dataframe containing entries from all time
        y (int or string): desired year

    Returns:
        DataFrame: dataframe containing entries for only the year specified'''

    y = str(y)

    jan1 = y+'-01-01'
    dec31 = y+'-12-31'

    ucase_date = 'Date'
    lcase_date = 'date'

    if ucase_date in df.columns:
        df = df.loc[(df[ucase_date]>=jan1) & (df[ucase_date] <= dec31)].reset_index(drop=True).copy()
    elif lcase_date in df.columns:
        df = df.loc[(df[lcase_date]>=jan1) & (df[lcase_date] <= dec31)].reset_index(drop=True).copy()

    return df

def drop_val_from_col(df,col,val):
    '''Drop entries of specific value from certain column.
    
    Args:
        df (DataFrame): complete dataframe
        col (str): name of column to look for val. Not case sensitive.
        val (any): rows containing val in col will be removed. Case sensitive
        
    Returns: 
        DataFrame: dataframe with rows containing val in col removed'''

    original_columns = df.columns
    df.columns = [x.lower() for x in df.columns]
    # df.drop(df.loc[df[col.lower()]==val].index,inplace=True)
    # df = df.reset_index(drop=True)
    df = df.loc[df[col.lower()] != val].reset_index(drop=True).copy()
    df[col.lower()] = df[col.lower()].astype(int)
    df.columns = original_columns
    return df

def column_sum(df,col):
    '''Find the sum of a column
    
    Args:
        df (DataFrame): dataframe containing all data
        col (str): name of column to be summed
        
    Returns:
        int: sum of column'''

    return df[col].sum()

def total_birds_counted(df):
    ''' Find the total number of birds counted. Requires count column to be summable, and 
    all "present" entries have been removed.
    
    Args:
        df (DataFrame): dataset
    Returns: no return. output is printed to terminal'''

    'Drop entries containing "X" for the count, which denotes a bird was present, but not counted.'
    df = drop_val_from_col(df,'count','X')
    df['count'] = df['count'].astype(int)
    total_birds = column_sum(df,'count')
    print('\n{:,} birds were counted.\n'.format(total_birds))

def most_freq_bird(df,n=10):
    '''Find the birds that showed up on the most checklists for a given dataset.
    Args:
        df (DataFrame): dataset
        n (int): number of birds to show in output (default = 10)
        
    Returns:
        no return. Prints output to terminal'''

    number_of_checklists = len(df['id'].unique())
    # 'time' column here is arbitrary. Just want to to end up with another column named 'count'
    freq_bird = df.groupby('common')['time'].count().reset_index(name='count')
    freq_bird.set_index('common',inplace=True)
    freq_bird['perc_of_checklists'] = (freq_bird['count'] / number_of_checklists) * 100
    freq_bird['perc_of_checklists'] = freq_bird['perc_of_checklists'].round(1)

    t = '\nMost frequently seen birds in {:,} checklists:\n{}\n'
    freq_bird = freq_bird.sort_values(by='count',ascending=False).head(n)

    print(t.format(number_of_checklists,freq_bird))

def main():
    '''Main function calling other functions.
    Args: no args
    Returns: no return'''

    df = read_data('MyEBirdData.csv')
    # df = read_data(r'test_read_csv.csv',date_and_time_column_positions=[3,4])
    # print(df.iloc[0:3].head())
    # print(focus_on_year(df,2020))
    # exit()
    cols_to_keep = ['date_and_time','Submission ID','Common Name','Count',
    'State/Province','County','Location','Date','Time']
    df = keep_columns(df,cols_to_keep)
    df = rename_and_lcase_columns(df,{'Submission ID':'id','Common Name':'common','State/Province':'state'})
    df_2021 = focus_on_year(df,2021)

    total_birds_counted(df_2021)
    most_freq_bird(df_2021)

    print(df_2021['date'].min())

if __name__ == '__main__':
    main()