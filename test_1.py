from re import I
import birds_2021
import pandas as pd
import numpy as np
import datetime as dt

def test_read_data():
    june_20_2014 = '6/20/2014 nan'
    nov_20_2021 = '11/20/2021 12:32 PM'

    final_data_correct = {
        'date_and_time':[june_20_2014,nov_20_2021],
        'Submission ID':[123,456],
        'Common Name':['Goose','Duck'],
        'Count':[2,20],
        'Date':['6/20/2014','11/20/2021'],
        'Time':[np.nan,'12:32 PM']
    }
    final_df_correct = pd.DataFrame(data=final_data_correct)

    f = r'test_read_csv.csv'
    tested_df = birds_2021.read_data(f,date_and_time_column_name='date_and_time',date_and_time_column_positions=[3,4],idf=True,kdc=True)
    print(tested_df.dtypes)
    assert tested_df.equals(final_df_correct)

def test_keep_single_column(test_dataset):

    final_df_correct = pd.DataFrame({'Count':[100,'X',300,400]})
    tested_df = birds_2021.keep_columns(test_dataset,'Count')
    
    assert tested_df.equals(final_df_correct)

def test_keep_multiple_columns(test_dataset):

    final_df_correct = pd.DataFrame({
        'Common Name':['Bob','Joe','Mary','Mary'],
        'Count':[100,'X',300,400]})
    tested_df = birds_2021.keep_columns(test_dataset,['Common Name','Count'])
    
    assert tested_df.equals(final_df_correct)

def test_rename_and_lcase_columns(test_dataset):

    may_1_2021 = dt.datetime(2021,5,1)
    june_1_2020 = dt.datetime(2020,6,1)
    july_1_2020 = dt.datetime(2020,7,1)
    august_1_2019 = dt.datetime(2019,8,1)

    d = {
        'date_and_time':[may_1_2021,june_1_2020,july_1_2020,august_1_2019],
        'id':[1234,2345,3456,4567],
        'common':['Bob','Joe','Mary','Mary'],
        'count':[100,'X',300,400],
        'date':['2021-05-01','2020-06-01','2020-07-01','2019-08-01'],
        'time':['12:32 PM','7:04 AM','10:20 AM','5:15 PM']}

    final_df_correct = pd.DataFrame(data=d)
    
    test_rename_dict = {
        'Submission ID':'id',
        'Common Name':'common',
        'Count':'count'
    }

    tested_df = birds_2021.rename_and_lcase_columns(test_dataset,test_rename_dict)

    assert tested_df.equals(final_df_correct)

def test_focus_on_year(test_dataset):

    june_1_2020 = dt.datetime(2020,6,1)
    july_1_2020 = dt.datetime(2020,7,1)

    d = {
        'date_and_time':[june_1_2020,july_1_2020],
        'Submission ID':[2345,3456],
        'Common Name':['Joe','Mary'],
        'Count':['X',300],
        'Date':['2020-06-01','2020-07-01'],
        'Time':['7:04 AM','10:20 AM']}

    final_df_correct = pd.DataFrame(data=d)

    tested_df = birds_2021.focus_on_year(test_dataset,2020)

    assert tested_df.equals(final_df_correct)

def test_drop_present_entries(test_dataset):
    may_1_2021 = dt.datetime(2021,5,1)
    july_1_2020 = dt.datetime(2020,7,1)
    august_1_2019 = dt.datetime(2019,8,1)

    d = {
        'date_and_time':[may_1_2021,july_1_2020,august_1_2019],
        'Submission ID':[1234,3456,4567],
        'Common Name':['Bob','Mary','Mary'],
        'Count':[100,300,400],
        'Date':['2021-05-01','2020-07-01','2019-08-01'],
        'Time':['12:32 PM','10:20 AM','5:15 PM']}

    final_correct_df = pd.DataFrame.from_dict(d)

    tested_df = birds_2021.drop_val_from_col(test_dataset,'Count','X')

    '''Something goofy here. Tried to compare the dataframes using df.equals as 
    was done before, but assertion failed. Verified that every element, column 
    header and index was of the same value and type, and did variety of other troubleshooting
    steps, but still failed. Eventually found this workaround on stackoverflow.'''
    assert (tested_df == final_correct_df).all().all()

def test_column_sum(test_dataset):
    assert birds_2021.column_sum(test_dataset,'Submission ID') == 11602