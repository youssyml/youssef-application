FROM --platform=linux/amd64 python:3.10.9-bullseye

WORKDIR /app

COPY streamlit/assets assets
COPY streamlit/.streamlit .streamlit
COPY streamlit/pages streamlit/pages
COPY streamlit/Alan_reviews_👀.py streamlit/requirements.txt streamlit/
RUN pip3 install -r streamlit/requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "streamlit/Alan_reviews_👀.py", "--server.port=8080", "--server.address=0.0.0.0"]
