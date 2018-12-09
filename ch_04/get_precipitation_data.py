import requests
import pandas as pd

def make_request(endpoint, payload=None):
    """Make a request to a specific endpoint on the weather API
    passing headers and optional payload."""
    return requests.get(
        f'https://www.ncdc.noaa.gov/cdo-web/api/v2/{endpoint}',
        headers={
            'token': 'PASTE_YOUR_TOKEN_HERE'
        },
        params=payload
    )

if __name__ == '__main__':
    response = make_request(
        'data', 
        {
            'datasetid' : 'GHCND',
            'locationid' : 'CITY:US360019',
            'stationid' : 'GHCND:US1NJBG0003',
            'startdate' : '2018-10-01',
            'enddate' : '2018-11-25',
            'datatypeid' : 'PRCP', 
            'units' : 'metric',
            'limit' : 1000
        }
    )

    if response.ok:
        df = pd.DataFrame(response.json()['results'])
        df = df.assign(
            date=pd.to_datetime(df.date)
        ).pivot(
            index='date',
            columns='datatype',
            values='value'
        ).reset_index()
        df.columns.rename('', inplace=True)
        df.to_csv('precipitation.csv', index=False)
    else:
        print(f'Unable to get result from API, status: {response.status_code}')
