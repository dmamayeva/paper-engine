import ingest
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os
from pathlib import Path
import os
from dotenv import load_dotenv
import sys 

project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / '.envrc')


client = OpenAI()
es_client = ingest.load_data()
index_name = ingest.index_name

def format_docs(docs):
    return "\n\n".join(doc['text'] for doc in docs)

def build_prompt(query, search_results):
    prompt_template = """
    You're a helpful deep learning mentor. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.
    
    QUESTION: 
    {question}
    CONTEXT: 
    {context}
    """.strip()

    context = format_docs(search_results)
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def elastic_search(query, boost=None):
    if boost is None:
        boost = {"query": query}
        size = 5
    else:
        size = boost['size']
        boost_dict = {"query": query,
                 "fields": [f"text^{boost['field']}"]}
    search_query = {
        "size": size,
        "query": {
            "bool": {
                "must": {
                    "multi_match": boost_dict,
                },
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs

def rag(query):
    search_results = elastic_search(query, {'field': 4, 'size': 9})
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer
