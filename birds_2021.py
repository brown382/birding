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

def filter_by_dates(df,start_date,end_date,year):
    '''Filter dataframe for a specific year, using the date column
    Args:
        df (DataFrame): dataframe containing entries from all time
        start_date (str): if not None (default), drop all data before this date. Must be str in yyyy-mm-dd format.
        end_date (str): if not None (default), drop all data after this date. Must be str in yyyy-mm-dd format.
        year (int): if not None (default), drop all data not in this year

    Returns:
        DataFrame: dataframe containing entries for only the year specified'''

    'If user wants to examine entire dataset and not filter by date'
    if sum(x is not None for x in [start_date,end_date,year]) == 0:
        return df

    date_col = [x for x in df.columns if x in ['date','Date']][0]

    'Check for invalid entries'
    if not year == None and (not start_date == None or not end_date == None):
        raise Exception("If providing start_date and/or end_date, cannot also provide year")

    #Year was provided
    if not year == None:
        start_date = str(year)+'-01-01'
        end_date = str(year)+'-12-31'
        df = df.loc[(df[date_col]>=start_date) & (df[date_col] <= end_date)].reset_index(drop=True).copy()
        return df
    #Both start and end dates were provided
    elif not start_date == None and not end_date == None:
        df = df.loc[(df[date_col]>=start_date) & (df[date_col] <= end_date)].reset_index(drop=True).copy()
        return df
    #Only start date was provided
    elif not start_date == None:
        df = df.loc[df[date_col]>=start_date].reset_index(drop=True).copy()
        return df
    #Only end date was provided
    elif not end_date == None:
        df = df.loc[df[date_col] <= end_date].reset_index(drop=True).copy()
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

def total_birds_counted(file,start_date=None,end_date=None,year=None):
    ''' Find the total number of birds counted. Requires count column to be summable, and 
    all "present" entries have been removed.
    
    Args:
        file (str): file path of dataset to be read
        start_date (str): str representation of start date by which to filter dates. Default
        is None.
        end_date (str): str representation of end date by which to filter dates. Default
        is None.
        year (int): data not in this year will be dropped from analyses. Default is None
    Returns:
        int: number of birds counted'''

    df = read_data(file)
    df = filter_by_dates(df, start_date=start_date, end_date=end_date, year=year)

    'Drop entries containing "X" for the count, which denotes a bird was present, but not counted.'
    count_col = [c for c in df.columns if c in ['count','Count']][0]
    df = drop_val_from_col(df,count_col,'X')

    df[count_col] = df[count_col].astype(int)
    total_birds = column_sum(df,count_col)

    return total_birds

def most_freq_bird(file,n=None,start_date=None,end_date=None,year=None):
    '''Find the birds that showed up on the most checklists for a given dataset.
    Args:
        file (str): file path of dataset to be read
        n (int): number of birds to show in output. Default = None (return all results)
        start_date (str): str representation of start date by which to filter dates. Default
        is None.
        end_date (str): str representation of end date by which to filter dates. Default
        is None.
        year (int): data not in this year will be dropped from analyses. Default is None        
        
    Returns:
        number_of_checklists (int): number of checklists in datasetno return. Prints output to terminal'''

    df = read_data(file)
    df = filter_by_dates(df, start_date=start_date, end_date=end_date, year=year)

    total_number_of_checklists = len(df['Submission ID'].unique())
    # 'Count' column here is arbitrary. Just want to to end up with another column named 'count'
    freq_bird = df.groupby('Common Name')['Count'].count().reset_index(name='num_checklists')
    freq_bird.set_index('Common Name',inplace=True)
    freq_bird['perc_of_checklists'] = (freq_bird['num_checklists'] / total_number_of_checklists)

    freq_bird = freq_bird.sort_values(by='num_checklists',ascending=False)
    if not n == None:
        freq_bird = freq_bird.iloc[:n].copy()

    return total_number_of_checklists, freq_bird

# def main():
#     '''Main function calling other functions.
#     Args: no args
#     Returns: no return'''

#     df = read_data('MyEBirdData.csv')
#     cols_to_keep = ['date_and_time','Submission ID','Common Name','Count',
#     'State/Province','County','Location','Date','Time']
#     df = keep_columns(df,cols_to_keep)
#     df = rename_and_lcase_columns(df,{'Submission ID':'id','Common Name':'common','State/Province':'state'})
#     df_2021 = filter_by_dates(df,2021)

#     total_birds_counted(df_2021)
#     most_freq_bird(df_2021)

# if __name__ == '__main__':
#     main()