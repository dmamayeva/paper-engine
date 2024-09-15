import pandas as pd
from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings
import os 
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent

# Elastic Search Connection

index_name = "article_info"

def load_data(path='article_info.csv', index_name="article_info"):
    # ingesting data
    es_client = Elasticsearch('http://localhost:9200') 
    
    df = pd.read_csv(path)
    df.drop('Unnamed: 0', axis=1, inplace=True)

    documents = df.to_dict(orient='records')
    for doc in tqdm(documents):
        es_client.index(index=index_name, document=doc)
    
    return es_client

    