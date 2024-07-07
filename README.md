Introduction
=============
This project gathers SEO data and analyzes them, providing valuable data and insights. This project first hits the the dataforseo API to gather data about the provided keywords. Then we use an LLM and huggingface to creating embeding for the keywords. We utilize those embeddings to cluster those keywords into different groups. Lastly we analyze this data to provide valuable insights. 


Installation
=============

#### Python
- `$ git clone https://github.com/abdullahtarek/seo_keyword_analysis.git`
- `$ cd seo_keyword_analysis`
- `$ pip install -r requirements.txt`
- `$ python keyword_analysis.py`

#### Docker
- `$ git clone https://github.com/abdullahtarek/seo_keyword_analysis.git`
- `$ cd seo_keyword_analysis`
- `$ docker build . -t keyword_analysis`
- `$ docker run keyword_analysis -v $(pwd)/output:/root/app/output -v $(pwd)/.env:/root/app/.env`
