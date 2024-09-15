FROM python:3.12-slim

WORKDIR /app

RUN pip install pipenv 

COPY notebooks/article_info.csv article_info.csv
COPY notebooks/ground_truth_data.csv ground_truth_data.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY app .

EXPOSE 8501

CMD ["pipenv", "run", "streamlit", "run", "app.py"]