FROM --platform=linux/amd64 python:3.10.9-bullseye
COPY nlp nlp
COPY data/processed_reviews.csv data/processed_reviews.csv
RUN pip install -r nlp/requirements.txt
RUN spacy download "fr_core_news_sm"
CMD uvicorn nlp.fast:app --host 0.0.0.0 --port $PORT
