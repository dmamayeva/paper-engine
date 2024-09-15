import os
import requests
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
from dotenv import load_dotenv
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent

from db import init_db

load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL")
INDEX_NAME = os.getenv("INDEX_NAME")



def fetch_documents():
    df = pd.read_csv(project_root/"notebooks/article_info.csv")
    df.drop('Unnamed: 0', axis=1, inplace=True)
    documents = df.to_dict(orient='records')

    print(f"Fetched {len(documents)} documents")
    return documents


def fetch_ground_truth():
    print("Fetching ground truth data...")
    df_ground_truth = pd.read_csv(project_root/"notebooks/ground_truth_data.csv")
    df_ground_truth.drop('Unnamed: 0', axis=1, inplace=True)

    ground_truth = df_ground_truth.to_dict(orient="records")
    print(f"Fetched {len(ground_truth)} ground truth records")

    return ground_truth



def setup_elasticsearch():
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "source": {"type": "text"},
                "page": {"type": "integer"},
                "id": {"type": "integer"} 
            }
        }
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client


def index_documents(es_client, documents):
    print("Indexing documents...")
    for doc in tqdm(documents):
        es_client.index(index=INDEX_NAME, document=doc)
    print(f"Indexed {len(documents)} documents")


def main():
    # you may consider to comment <start>
    # if you just want to init the db or didn't want to re-index
    print("Starting the indexing process...")

    documents = fetch_documents()
    ground_truth = fetch_ground_truth()
    es_client = setup_elasticsearch()
    index_documents(es_client, documents)
    # you may consider to comment <end>

    print("Initializing database...")
    init_db()

    print("Indexing process completed successfully!")


if __name__ == "__main__":
    main()