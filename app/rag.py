import ingest
import time
from pathlib import Path
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
load_dotenv('.envrc')


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
    
    return response

def evaluate(question, response):
    rag_prompt_template = """
            You are an expert evaluator for a RAG system.
            Your task is to analyze the relevance of the generated answer to the given question.
            Based on the relevance of the generated answer, you will classify it
            as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

            Here is the data for evaluation:

            Question: {question}
            Generated Answer: {answer_llm}

            Please analyze the content and context of the generated answer in relation to the question
            and provide your evaluation in parsable JSON without using code blocks:

            {{
            "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
            "Explanation": "[Provide a brief explanation for your evaluation]"
            }}
            """.strip()
    prompt = rag_prompt_template.format(question=question, 
                                        answer_llm=response.choices[0].message.content)
    answer = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )

    relevant = json.loads(answer.choices[0].message.content)
    return relevant, answer

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
    t0 = time.time()
    search_results = elastic_search(query, {'field': 4, 'size': 9})
    prompt = build_prompt(query, search_results)
    response = llm(prompt)
    relevance, eval_response = evaluate(query, response)
    relevance_keys = list(relevance.keys())
    t1 = time.time()
    answer = {
        'answer': response.choices[0].message.content,
        'response_time': t1-t0,
        'relevance': relevance[relevance_keys[0]],
        'relevance_explanation': relevance[relevance_keys[1]],
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens,
        'eval_prompt_tokens': eval_response.usage.prompt_tokens,
        'eval_completion_tokens': eval_response.usage.completion_tokens,
        'eval_total_tokens': eval_response.usage.total_tokens,
        'openai_cost': (1.5e-7*int(response.usage.total_tokens)) + (1.5e-7*int(eval_response.usage.total_tokens)),
        
    }
    return answer
