from fastapi import FastAPI
from nlp.nlp import NLP
from datetime import datetime

app = FastAPI()

app.state.model = NLP()


@app.get("/reviews")
async def get_reviews(start: str, end: str):
    """
    Returns all reviews and their rating between two dates
    """
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    response = app.state.model.get_reviews(start, end)
    print(response)

    return {"reviews": app.state.model.get_reviews(start, end)}


@app.get("/reviews/sw")
async def get_sw(start: str, end: str):
    """
    Returns the strengths and weaknesses between two dates
    """
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    return app.state.model.get_strength_weaknesses(start, end)


@app.get("/reviews/clusters")
async def get_clusters(start: str, end: str):
    """
    Returns the meta data about the clusters
    """
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    return app.state.model.get_clusters(start, end)
