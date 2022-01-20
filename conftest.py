import pytest
import pandas as pd
import datetime as dt

@pytest.fixture
def test_dataset():

    may_1_2021 = dt.datetime(2021,5,1)
    june_1_2020 = dt.datetime(2020,6,1)
    july_1_2020 = dt.datetime(2020,7,1)
    august_1_2019 = dt.datetime(2019,8,1)

    d = {
        'date_and_time':[may_1_2021,june_1_2020,july_1_2020,august_1_2019],
        'Submission ID':[1234,2345,3456,4567],
        'Common Name':['Bob','Joe','Mary','Mary'],
        'Count':[100,'X',300,400],
        'Date':['2021-05-01','2020-06-01','2020-07-01','2019-08-01'],
        'Time':['12:32 PM','7:04 AM','10:20 AM','5:15 PM']}

    df = pd.DataFrame(data=d)

    return df