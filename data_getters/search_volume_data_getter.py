import requests
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


class SearchVolumeDataGetter():
    def __init__(self):
        self.batch_size=1000

    def call_api(self, keywords):
        url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
        headers = {
            'Authorization': os.getenv('DATAFORSEO_BASIC_AUTH'),
            'Content-Type': 'application/json'
        }

        keywords_str = '"' + '","'.join(keywords) + '"'
        payload="[{\"keywords\":["+keywords_str+"], \"location_code\":2826, \"sort_by\":\"relevance\"}]"
        
        response = requests.request("POST", url, headers=headers, data=payload)
       

        return response

    def parse_response(self,response):        
        output_list =  []
        for keyword_result in response.json()['tasks'][0]['result']:
            keyword= keyword_result['keyword']
            competition = keyword_result['competition']
            competition_index = keyword_result['competition_index']
            search_volume = keyword_result['search_volume']
            cpc = keyword_result['cpc']

            row_dict = {
                'keyword': keyword,
                'competition': competition,
                'competition_index': competition_index,
                'search_volume': search_volume,
                'cpc': cpc
            }

            output_list.append(row_dict)
            
        return output_list

    def get_data(self, keywords):
        
        # divide keywwords list into batches
        keyword_batches = [keywords[i:i+self.batch_size] for i in range(0, len(keywords), self.batch_size)]

        
        # Run Batches through the API
        output_list = []
        for keyword_batch in keyword_batches:
            response = self.call_api(keyword_batch)
            if response.status_code != 200:
                raise Exception("API call failed with status code: " + str(response.status_code))
            wrangled_data = self.parse_response(response)
            output_list+= wrangled_data

        search_volume_df  = pd.DataFrame(output_list)
        
        return search_volume_df
