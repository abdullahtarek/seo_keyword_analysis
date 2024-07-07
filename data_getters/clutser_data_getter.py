from .embedding_data_getter import EmbeddingDataGetter
from sklearn.cluster import AffinityPropagation
import numpy as np

class ClusterDataGetter():
    def __init__(self):
        self.cluster_names = {
            "content feedback":"Content Strategy and Management",
            "cloud based collaboration":"Collaborative Tools and Solutions",
            "international seo":"Global SEO Strategies",
            "bulk edit attributes woocommerce":"Bulk Editing Solutions",
            "woocommerce discount rules":"Discount and Pricing Solutions",
            "wordpress attacks":"Security and Protection",
            "woocommerce metadata":"Content and Metadata Management",
            "multilingual social media":"Multilingual Toolbox"
        }

    def get_data(self, keywords):
        embedding_data_getter = EmbeddingDataGetter()
        embeddings_df = embedding_data_getter.get_data(keywords)

        # Convert embeddings to a numpy array
        X = np.array(embeddings_df['embeddings'].tolist())

        # Perform Affinity Propagation clustering
        affinity_propagation = AffinityPropagation().fit(X)

        # Plot the clustering result
        labels = affinity_propagation.labels_
        
        embeddings_df['cluster_int'] = labels

        embeddings_df['cluster_name']='no_name'
        for sample_keyword, cluster_name in self.cluster_names.items():
            cluster_int = embeddings_df[embeddings_df['keyword']==sample_keyword]['cluster_int'].values[0]
            embeddings_df.loc[embeddings_df['cluster_int']==cluster_int,'cluster_name']=cluster_name

        return embeddings_df
