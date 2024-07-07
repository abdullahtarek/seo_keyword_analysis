import pickle
import os 
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

class TrendDataGetter():
    def __init__(self):
        self.batch_size=5

    def call_api(self, keywords,keyword_batch_ind):    
        url = "https://api.dataforseo.com/v3/keywords_data/dataforseo_trends/explore/live"
        headers = {
            'Authorization': os.getenv('DATAFORSEO_BASIC_AUTH'),
            'Content-Type': 'application/json'
        }

        keywords_str = '"' + '","'.join(keywords) + '"'
        payload="[{\"time_range\":\"past_12_months\",\"keywords\":["+keywords_str+"] }]"

        response = requests.request("POST", url, headers=headers, data=payload)

        return response

    def parse_response(self,response):
        keyword_result = response.json()['tasks'][0]['result'][0]        
        keyword_batch_list = keyword_result['items'][0]['keywords']

        output_list = []
        for date_index , date_data in enumerate(keyword_result['items'][0]['data']):
            time_period = f'time_period_{date_index:02}'
            for keyword_index , date_value in enumerate(date_data['values']):
                output_dict = {'keyword':keyword_batch_list[keyword_index]}
                output_dict['time_period'] = time_period
                output_dict['value'] = date_value
                output_list.append(output_dict)
            
        return output_list

    def get_data(self, keywords):
        
        # divide keywwords list into batches
        keyword_batches = [keywords[i:i+self.batch_size] for i in range(0, len(keywords), self.batch_size)]
        
        # Run Batches through the API
        output_list = []
        responses = []
        for keyword_batch_ind , keyword_batch in enumerate(keyword_batches):
            response = self.call_api(keyword_batch,keyword_batch_ind)
            responses.append(response)
            if response.status_code != 200:
                raise Exception("API call failed with status code: " + str(response.status_code))
            wrangled_data = self.parse_response(response)
            output_list+= wrangled_data

        # Change output to DataFrame
        trend_data_df = pd.DataFrame(output_list)

        # Calculate moving Average of the trend data differences
        diff_df = trend_data_df.groupby('keyword')['value'].diff().fillna(0)
        trend_data_df['diff'] = diff_df
        trend_data_df = trend_data_df.sort_values(by=['keyword', 'time_period'])
        trend_data_df['trend'] = trend_data_df['diff'].rolling(window=10).mean()

        # Add a Row Number to know which row is the last row of the time period
        trend_data_df['row_number'] = trend_data_df.groupby('keyword').cumcount() + 1
        trend_data_df = trend_data_df.sort_values(by=['keyword', 'time_period'])

        # Get the Last row of this time period
        trend_data_df = trend_data_df[trend_data_df['time_period']=='time_period_50'][['keyword','trend']]
        
        return trend_data_df
