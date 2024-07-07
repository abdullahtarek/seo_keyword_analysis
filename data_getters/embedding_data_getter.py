from sentence_transformers import SentenceTransformer
import pandas as pd

class EmbeddingDataGetter():
    def __init__(self):
        self.LLM_name= 'Salesforce/SFR-Embedding-2_R'
        self.LLM = SentenceTransformer(self.LLM_name)
    
    def get_data(self, keywords):
        keywords = [keyword.lower() for keyword in keywords]
        keyword_embeddings = self.LLM.encode(keywords)
        embedding_dataframe = pd.DataFrame({'keyword':keywords,
              'embeddings': keyword_embeddings.tolist() 
              })

        return embedding_dataframe