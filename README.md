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

## Usage

To manage dependencies, **pipenv** and **python 3.12** is used. 

To install pipenv (in case of abscence):

```bash
pip install pipenv
```
and then

```bash
pipenv install
```

Running Jupyter notebooks for experiments and see the dataset generation 
```bash
cd notebooks
pipenv run jupyter notebook
```

## Evaluation 
### Retrieval


### RAG flow

## Monitoring

## Ingestion 

