import streamlit as st

st.set_page_config(
    page_title="Read me 📑",
    page_icon="assets/alan.png",
)

st.title("Read me 📑")

st.markdown(
    """
            The purpose of this application is to demonstrate my **motivation to join Alan** and give
            a glimpse of my **technical skills**. It was really fun to build, I hope you enjoy it as well 😊.
            """
)

st.markdown(
    """
            ## Source code 🧑‍💻
            To check out the code, head over to [my github](https://github.com/youssyml/alan-application).
            The code base is entirely in Python 🐍
    """
)


st.markdown(
    """
            ## Getting the data 🤖
            To get Alan's reviews on google map, I have built a scrapper using **Selenium**. \n
            The scrapper opens google maps, goes to Alan's reviews page, scrolls to the bottom and gets
            all reviews along with relevant information (star rating etc.) \n
            The HTML was then parsed using BeautifulSoup.
            """
)

st.markdown(
    """
            ## Analyzing the data 📊
            The most interesting part of the analysis is **topic extraction** from the reviews. The method I used
            consists in 3 main steps:
            1. Text preprocessing
            2. Building **clusters** of reviews
            3. Extracting representative **topics** from the clusters.

            #### Text preprocessing 🧹
            Only french reviews were kept. The text was first stripped of special characters and
            digit. Then, I lemmatized it using **spacy**.

            #### Building clusters 👀
            I used two approaches to build the clusters:
            1. Manually splitting the reviews in two groups : reviews with 1-2 stars and reviews with 4-5 stars.
            Extracting topics from these two groups allowed me to identify Alan's strengths and improvement areas.
            2. Using an embedding from [SBERT](https://www.sbert.net/). The embedding is a numerical representation of each review in 512 dimensions. I used [UMAP](https://umap-learn.readthedocs.io/en/latest/) to recude the dimensions to 10 and then used the [HDBSCAN algorithm](https://hdbscan.readthedocs.io/en/latest/) to cluster the reviews.

            #### Extracting topics from the clusters 🕵️‍♀️
            I computed a [C-TF-IDF](https://maartengr.github.io/BERTopic/api/ctfidf.html) for trigrams in the reviews using scikit-learn CountVectorizer. The top 3 trigrams are returned for each cluster.
            """
)

st.markdown(
    """
            ## Building the product 🛠️
            The final product is made of 2 main components:
            - This **streamlit** application
            - An API built with **FastAPI** with 3 endpoints to serve the review data to the streamlit application.
            Each endpoint takes a review start and end date as query parameters.

            Both components were containerized using **Docker** and deployed on **Google Cloud** (Cloud Run)

            """
)
