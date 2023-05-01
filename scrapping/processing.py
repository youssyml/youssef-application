from bs4 import BeautifulSoup
import pickle
import csv


def get_stars_count(review_soup):
    return len(
        review_soup.find("span", class_="kvMYJc").find_all(
            "img", class_="hCCjke vzX5Ic"
        )
    )


def get_review_metadata(review_soup):
    metadata = review_soup.find("div", class_="MyEned")
    if not metadata:
        return {"id": "", "lang": ""}
    return {"id": metadata.get("id"), "lang": metadata.get("lang")}


def get_review_text(review_soup):
    elem = review_soup.find("div", class_="MyEned")
    if not elem:
        return ""
    return elem.find("span", class_="wiI7pd").text


def get_review_date(review_soup):
    return review_soup.find("span", class_="rsqaWe").text


def process_reviews(reviews: list) -> list:
    """
    Processes the list of reviews
    """
    processed_reviews = []
    for review in reviews:
        review_soup = BeautifulSoup(review, "html.parser")
        star_count = get_stars_count(review_soup)
        metadata = get_review_metadata(review_soup)
        text = get_review_text(review_soup)
        time_ago = get_review_date(review_soup)
        processed_reviews.append(
            {
                "stars": star_count,
                "id": metadata.get("id"),
                "lang": metadata.get("lang"),
                "text": text,
                "time_ago": time_ago,
            }
        )

    return processed_reviews


if __name__ == "__main__":
    with open("data/reviews_raw.pickle", "rb") as f:
        reviews = pickle.load(f)

    processed_reviews = process_reviews(reviews)

    with open("data/processed_reviews.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=list(processed_reviews[0].keys()))
        writer.writeheader()
        writer.writerows(processed_reviews)
