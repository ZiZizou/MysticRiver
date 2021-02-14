import pandas as pd
from sodapy import Socrata
import os

path = './data.csv'

def get_data(selection, update, results):
    if(update and os.path.exists(path)):
        print('please wait while we source the data')
        client = Socrata("data.calgary.ca", None)
        results = client.get("5fdg-ifgr", limit=results)
        results_df = pd.DataFrame.from_records(results)
        results_df.to_csv(path)
    
    results_df = pd.read_csv(path)

    results_df = results_df.loc[results_df['station_name']==selection]
    results_df = results_df.loc[results_df['level']!='NA']
    timestamps = results_df['timestamp'].tolist()
    dates = [timestamps[x][:10] for x in range(len(timestamps))]
    results_df = results_df[['level']]

    results_df = results_df.astype(float)
    results_df['date'] = dates

    dates = list(set(dates))
    print(f'{len(dates)} dates have been retrieved from the database')
    dates.sort()
    print(f'{dates[0]},{dates[1]}, {dates[2]} .... to {dates[-2]}, {dates[-1]}')
    #print(dates)

    data = []
    for date in dates:
        ndf = results_df.loc[results_df['date']==date]
    #print(type(results_df.iloc[0, 1]),results_df.iloc[0, 1])
        data.append((ndf['level'].mean(),date))
    final_df = pd.DataFrame(data, columns = ['y', 'ds'])
    final_df['ds'] = pd.to_datetime(final_df['ds'])
    return final_df