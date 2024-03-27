import pandas as pd
from datetime import datetime
import requests
import json


class Core:


    def __init__(self):
        
        self.neo_data = pd.read_excel('data/neo_data.xlsx', engine='openpyxl')
        self.neo_close_data = pd.read_excel('data/neo_close_data.xlsx', engine='openpyxl')
        self.neos = None
        self.sentry = None
        self.h_mag = None
        self.min_diam = None
        self.min_diam_obj = None
        self.max_diam = None
        self.max_diam_obj = None
        self.hazard = None
        self.max_miss = None
        self.max_miss_obj = None
        self.min_miss = None
        self.min_miss_obj = None
        self.max_vel = None
        self.max_vel_obj = None
        self.min_vel = None
        self.min_vel_obj = None


    def get_data(self, start_date, end_date):
        
        API_KEY=''   # remove before commit and replace with env variable
        
        response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={key}'.format(start_date=start_date, end_date=end_date, key=API_KEY))
        response = json.loads(response.text)['near_earth_objects']
        data = pd.DataFrame(columns=['Date', 'ID', 'NEO Reference ID', 'Name', 'Absolute Magnitude H', 'Min Estimated Diameter (km)', 'Max Estimated Diameter (km)',
                            'Potentially Hazardous', 'Relative Velocity (km/s)', 'Miss Distance (au)', 'Orbiting Body', 'Sentry Object'])
        date_range = [datetime.now() - timedelta(days=i) for i in range(1, 8)]
        date_range = sorted(date_range)
        date_range = [x.strftime("%Y-%m-%d") for x in date_range]
        for date in date_range:
            for r in response[date]:
                data.loc[len(data.index)] = [date, r['id'], r['neo_reference_id'], r['name'], r['absolute_magnitude_h'], r['estimated_diameter']['meters']['estimated_diameter_min'],
                r['estimated_diameter']['meters']['estimated_diameter_max'], r['is_potentially_hazardous_asteroid'], r['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
                r['close_approach_data'][0]['miss_distance']['kilometers'], r['close_approach_data'][0]['orbiting_body'], r['is_sentry_object']]
        data['ID'] = data['ID'].apply(lambda x: str(x))
        data['NEO Reference ID'] = data['NEO Reference ID'].apply(lambda x: str(x))
        data.to_excel('data/neo_data.xlsx', index=False)

        obj_data = pd.DataFrame(columns=['ID', 'Close Approach Date', 'Relative Velocity (km/s)', 'Miss Distance (au)', 'Orbiting Body'])
        for id in pd.unique(data['ID']):
            lookup_response = requests.get('https://api.nasa.gov/neo/rest/v1/neo/{id}?api_key={key}'.format(id=id, key=API_KEY))
            lookup_response = json.loads(lookup_response.text)
            for closup in lookup_response['close_approach_data']:
                obj_data.loc[len(obj_data.index)] = [id, closup['close_approach_date'], closup['relative_velocity']['kilometers_per_second'], closup['miss_distance']['astronomical'], closup['orbiting_body']]
        obj_data['ID'] = obj_data['ID'].apply(lambda x: str(x))
        obj_data.to_excel('data/neo_close_data.xlsx', index=False)


    def set_metrics(self):

        self.neos = str(len(pd.unique(self.neo_data['ID'])))
        self.sentry = str(len(pd.unique(self.neo_data.loc[self.neo_data['Sentry Object']==True]['ID'])))
        self.hazard = str(len(pd.unique(self.neo_data.loc[self.neo_data['Potentially Hazardous']==True]['ID'])))
        self.h_mag = str(round((max(self.neo_data['Absolute Magnitude H']) + min(self.neo_data['Absolute Magnitude H'])) / 2, 2))
        self.min_diam = str(round(min(self.neo_data['Min Estimated Diameter (km)'].values), 2))
        self.max_diam = str(round(max(self.neo_data['Max Estimated Diameter (km)'].values), 2))
        self.min_miss = str(round(min(self.neo_data['Miss Distance (au)'].values), 2))
        self.max_miss = str(round(max(self.neo_data['Miss Distance (au)'].values), 2))
        self.min_vel = str(round(min(self.neo_data['Relative Velocity (km/s)'].values), 2))
        self.max_vel = str(round(max(self.neo_data['Relative Velocity (km/s)'].values), 2))

        self.min_diam_obj = self.neo_data.loc[self.neo_data['Min Estimated Diameter (km)']==min(self.neo_data['Min Estimated Diameter (km)'].values)].values[0]
        self.max_diam_obj = self.neo_data.loc[self.neo_data['Max Estimated Diameter (km)']==min(self.neo_data['Max Estimated Diameter (km)'].values)].values[0]
        self.min_miss_obj = self.neo_data.loc[self.neo_data['Miss Distance (au)']==min(self.neo_data['Miss Distance (au)'].values)].values[0]
        self.max_miss_obj = self.neo_data.loc[self.neo_data['Miss Distance (au)']==max(self.neo_data['Miss Distance (au)'].values)].values[0]
        self.min_vel_obj = self.neo_data.loc[self.neo_data['Relative Velocity (km/s)']==min(self.neo_data['Relative Velocity (km/s)'].values)].values[0]
        self.max_vel_obj = self.neo_data.loc[self.neo_data['Relative Velocity (km/s)']==max(self.neo_data['Relative Velocity (km/s)'].values)].values[0]


    def get_bar_chart_data(self):

        chart = pd.DataFrame(columns=['Date', 'Objects'])
        chart['Date'] = pd.unique(self.neo_data['Date'])
        chart['Object Count'] = chart['Date'].apply(lambda x: len(pd.unique(self.neo_data.loc[self.neo_data['Date']==x]['ID'])))
        chart['Objects'] = chart['Date'].apply(lambda x: ', '.join(pd.unique(self.neo_data.loc[self.neo_data['Date']==x]['ID'].apply(lambda x: str(x)))))
        chart['Min Estimated Diameter (km)'] = chart['Date'].apply(lambda x: round(min(self.neo_data.loc[self.neo_data['Date']==x]['Min Estimated Diameter (km)'].values), 2))
        chart['Max Estimated Diameter (km)'] = chart['Date'].apply(lambda x: round(max(self.neo_data.loc[self.neo_data['Date']==x]['Max Estimated Diameter (km)'].values), 2))
        chart['Min Miss Distance (au)'] = chart['Date'].apply(lambda x: round(min(self.neo_data.loc[self.neo_data['Date']==x]['Miss Distance (au)'].values), 2))
        chart['Max Miss Distance (au)'] = chart['Date'].apply(lambda x: round(max(self.neo_data.loc[self.neo_data['Date']==x]['Miss Distance (au)'].values), 2))
        chart['Min Relative Velocity (km/s)'] = chart['Date'].apply(lambda x: round(min(self.neo_data.loc[self.neo_data['Date']==x]['Relative Velocity (km/s)'].values), 2))
        chart['Max Relative Velocity (km/s)'] = chart['Date'].apply(lambda x: round(max(self.neo_data.loc[self.neo_data['Date']==x]['Relative Velocity (km/s)'].values), 2))
        chart['Potentially Hazardous'] = chart['Date'].apply(lambda x: len(pd.unique(self.neo_data.loc[(self.neo_data['Date']==x) & (self.neo_data['Potentially Hazardous']==True)]['ID'])))
        chart['Sentry Objects'] = chart['Date'].apply(lambda x: len(pd.unique(self.neo_data.loc[(self.neo_data['Date']==x) & (self.neo_data['Sentry Object']==True)]['ID'])))

        chart['Date'] = chart['Date'].apply(lambda x: pd.to_datetime(x))
        chart.sort_values(by=['Date'], inplace=True)
        chart['Date'] = chart['Date'].apply(lambda x: x.strftime("%d-%b-%y"))

        return chart


    def get_scatter_chart_data(self):

        chart = pd.DataFrame(columns=['ID', 'Close Approach Year', 'Observation Count', 'Orbiting Body', 'Avg. Miss Distance (au)', 'Avg. Relative Velocity (km/s)'])
        chart['ID'] = self.neo_close_data['ID']
        chart['Orbiting Body'] = self.neo_close_data['Orbiting Body']
        chart['Close Approach Date'] = self.neo_close_data['Close Approach Date']
        chart['Close Approach Year'] = chart['Close Approach Date'].apply(lambda x: int(x.split("-")[0]))
        count = chart.groupby(['ID', 'Orbiting Body', 'Close Approach Year']).count()['Close Approach Date'].to_dict()
        chart['Observation Count'] = chart[['ID', 'Orbiting Body', 'Close Approach Year']].apply(lambda x: count[(x[0], x[1], x[2])], axis=1)
        chart.drop_duplicates(subset=['ID', 'Close Approach Year', 'Orbiting Body'], inplace=True)
        chart.drop(['Close Approach Date'], axis=1, inplace=True)
        self.neo_close_data['Close Approach Year'] = self.neo_close_data['Close Approach Date'].apply(lambda x: x.split("-")[0])
        chart['Avg. Miss Distance (au)'] = chart[['ID', 'Close Approach Year', 'Orbiting Body', 'Observation Count']].apply(lambda x: self.neo_close_data.loc[(self.neo_close_data['ID']==x[0]) & (self.neo_close_data['Close Approach Year']==x[1]) & (self.neo_close_data['Orbiting Body']==x[2])]['Miss Distance (au)'].sum() / x[3], axis=1)
        chart['Avg. Relative Velocity (km/s)'] = chart[['ID', 'Close Approach Year', 'Orbiting Body', 'Observation Count']].apply(lambda x: self.neo_close_data.loc[(self.neo_close_data['ID']==x[0]) & (self.neo_close_data['Close Approach Year']==x[1]) & (self.neo_close_data['Orbiting Body']==x[2])]['Relative Velocity (km/s)'].sum() / x[3], axis=1)

        return chart
