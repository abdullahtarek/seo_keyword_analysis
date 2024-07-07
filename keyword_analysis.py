import pandas as pd
from dotenv import load_dotenv
from data_getters import SearchVolumeDataGetter,TrendDataGetter,ClusterDataGetter
load_dotenv()

def main():
    df = pd.read_csv('data/keywords.csv')
    keywords = df['.htaccess'].tolist()

    data_getters = [SearchVolumeDataGetter,TrendDataGetter,ClusterDataGetter ]

    output_df = None
    for data_getter in data_getters:
        data_getter_instance = data_getter()
        data_df = data_getter_instance.get_data(keywords)
        
        if output_df is None:
            output_df =  data_df
        else: 
            output_df =  output_df.merge(data_df, on='keyword')
    
    output_df.drop(columns=['embeddings']).to_csv('output/output_df.csv',index=False)

if __name__ == '__main__':
    main()