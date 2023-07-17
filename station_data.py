import requests
import pandas as pd

def get_station_data():
    stations = requests.get('https://api.ust.is/aq/a/getStations').json()
    df = pd.DataFrame.from_dict(stations)
    df['parameters'] = df['parameters'].apply(lambda x: x.replace('{','').replace('}','').replace('"','').split(','))
    df = pd.concat([df.drop('parameters', axis=1),
                df['parameters'].apply(lambda x: pd.Series({item: 1 for item in x}))],
               axis=1)
    df.to_csv('raw_data/station_data.csv', index=False)
