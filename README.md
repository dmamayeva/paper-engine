# Paper-Engine: RAG Application for Deep Learning Papers

## Overview

**Paper-Engine** is a Retrieval-Augmented Generation (RAG) application designed to assist users in navigating and understanding key concepts in the deep learning domain. This project collects, formats, and organizes 100 essential deep learning papers, allowing users to interact with the system in a conversational manner and receive detailed responses from the content of these articles. 

---

## Problem Description

The field of deep learning is rapidly evolving, with a vast and growing number of research papers published every year. This presents several challenges:

1. **Retrieving Specific Information**: Find relevant information about specific topics from the large body of available literature is time-consuming.
3. **Need for Conversational Assistance**: Quick explanations or clarifications about complex deep learning concepts, which can be difficult to understand from research papers.

### Project Goal

Paper-Engine solves these problems by providing a way to:

- Efficiently retrieve deep learning information by leveraging a curated set of ~100 essential research papers.
- Offer conversational assistance for users seeking to learn or clarify deep learning concepts and models.

This enables users to engage with deep learning literature interactively, without the need to manually search through individual papers.

---

## Data

The dataset for Paper-Engine consists of about 100 seminal and recommended deep learning papers. These papers cover a wide range of topics, including:

- Core deep learning concepts and techniques
- Neural network architectures (CNNs, RNNs, Transformers, etc.)
- Optimization methods
- Recent advancements in generative models, reinforcement learning, and more

The papers are formatted from PDF into a text-friendly structure, enabling easy information retrieval and search within the content.

---

## Features

- **Conversational AI**: Users can ask questions and receive detailed answers based on the content of the 100 curated deep learning papers.
- **Information Retrieval**: Uses Retrieval-Augmented Generation (RAG) techniques to fetch relevant sections from the papers and generate answers.
- **Topic Coverage**: The system can assist with understanding a wide range of topics, including but not limited to:
  - Neural networks and deep learning architectures
  - Model training and optimization
  - Evaluation metrics and performance analysis
  - Emerging trends and research directions in deep learning

---
## Preparing the application 
Before running app, database should be initialized. 

To do that, run [`prep.py`](app/app.py) script
```bash
export POSTRES_HOST=localhost

cd app
pipenv run python prep.py
```
---
## Using application 

To run the application you can use one of two ways listed:
### Running it with Doker-compose 

To run this app with docker:

```bash
docker-compose up
```
### Running locally
#### Installing dependencies

In case if you don't like or use docker:
To manage dependencies, **pipenv** and **python 3.12** is used. 

To install pipenv (in case of abscence):

```bash
pip install pipenv
```
and then

```bash
pipenv install
```

Running streamlit application to check:
```bash
pipenv run streamlit run app/app.py
```
This command will open a web interface where you can ask questions and provide feedback for answers generated.

Running Jupyter notebooks for experiments and see the dataset generation 
```bash
cd notebooks
pipenv run jupyter notebook
```


## Evaluation

Evalutaion code is in the [notebooks/evaluation.ipynb](notebooks/evaluation.ipynb) notebook.
### Retrieval
Elastic Search and FAISS were tested.
The basic approach — without any boosting and *k=5* gave following results.
**Elastic Search**
* hit rate 0.798
* mrr 0.647

**FAISS**
* hit rate 0.758
* mrr 0.609



**Improved Elastic Search**
For the next experiments Elastic Search only is being used.
Achieved results for the field: ^4 and size=9
* hit_rate: 0.849
* mrr: 0.654

### RAG flow

For evaluation LLM-as-a-Judge (gpt-4o-mini-as-a-judge) was used. To reduce cost for OpenAI (next time going to try using open-source LLM) I used only gpt-4o-mini

In 432 processed records (errors in JSON formatting and wrong keys were ignored):

* Relevant: 423
* Partly relevant: 9
* Irrelevant: 0


## Monitoring

## Ingestion 

