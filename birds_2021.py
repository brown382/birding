'''
How many total birds did I see
What bird showed up most frequently on my checklists

'''

import pandas as pd

birds_original_dataset = pd.read_csv('MyEBirdData.csv',parse_dates={'date_and_time':[11,12]},
infer_datetime_format=True,keep_date_col=True)

cols_to_keep = ['date_and_time','Submission ID','Common Name','Count','State/Province','County','Location','Date','Time']
birds = birds_original_dataset[cols_to_keep].copy()

rename_cols = {'Submission ID':'id','Common Name':'common','State/Province':'state'}

birds = birds.rename(columns=rename_cols)
birds.columns = [x.lower() for x in birds.columns]

''' Drop entries prior to 2021, drop redundant date and time columns and 
clean date_and_time '''
birds.drop(birds.loc[birds['date']<'2021-01-01'].index,inplace=True)
birds.drop(columns=['date','time'],inplace=True)
birds['date_and_time'] = pd.to_datetime(birds['date_and_time'])
birds.rename(columns={'date_and_time':'time'},inplace=True)

''' Clean state column '''
birds['state'] = birds['state'].str[-2:]
birds['county_state'] = birds['county'] + ', ' + birds['state']
birds.drop(columns=['state','county'],inplace=True)

''' Answer total birds question '''

''' Clean count column '''
total_birds = birds.copy()

total_birds.drop(total_birds.loc[total_birds['count']=='X'].index,inplace=True)
total_birds['count'] = total_birds['count'].astype(int)

print('I reported {:,} birds in 2021.'.format(total_birds['count'].sum()))

''' Answer most frequently reported bird question '''

freq_bird = birds.copy()

number_of_checklists = len(freq_bird['id'].unique())

freq_bird = freq_bird.groupby('common')['time'].count().reset_index(name='count')
freq_bird['frequency'] = freq_bird['count'] / number_of_checklists
print(freq_bird.sort_values(by='count',ascending=False).head(25))