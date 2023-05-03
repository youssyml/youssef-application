import streamlit as st

st.set_page_config(
    page_title="Read me 📑",
    page_icon="assets/alan.png",
)

st.title("Read me 📑")

st.markdown(
    """
            The purpose of this application is to demonstrate my **motivation to join Alan** and give
            a glimpse of my **technical skills**. It was really fun to build, I hope you enjoy it as well 😊
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
            To get Alan's reviews on Google Maps, I have built a scrapper using **Selenium**. \n
            The scrapper opens Google Maps, goes to Alan's reviews page, scrolls to the bottom and gets
            all reviews along with relevant information (star rating, date) \n
            The HTML was then parsed using **BeautifulSoup**.
            """
)

st.markdown(
    """
            ## Analyzing the data 📊
            The most interesting part of the analysis is **topic extraction** from the reviews. The method I used
            consists in 3 main steps:

            #### 1- Text preprocessing 🧹
            Only french reviews were kept. I lowercased the text and stripped it of special characters and
            digits. I also lemmatized it using **spacy** and removed stop words.

            #### 2- Building clusters 👀
            I used two approaches to build clusters:
            1. Manually splitting the reviews in two groups : reviews with 1-2 star ratings and reviews with 4-5 star ratings.
            2. Performing unsupervised clustering using an embedding from [SBERT](https://www.sbert.net/).
            I used [UMAP](https://umap-learn.readthedocs.io/en/latest/) to recude the dimensions of the embedding and then used
            the [HDBSCAN algorithm](https://hdbscan.readthedocs.io/en/latest/) to cluster the reviews.

            #### 3- Extracting topics from the clusters 🕵️‍♀️
            I computed a [C-TF-IDF](https://maartengr.github.io/BERTopic/api/ctfidf.html) for trigrams in the reviews using
            **scikit-learn**'s CountVectorizer. The top 3 trigrams are displayed for each cluster.
            """
)

st.markdown(
    """
            ## Building the product 🛠️
            The final product is made of 2 main components:
            - This **streamlit** application
            - An API built with **FastAPI** with 3 endpoints to serve the review data to the streamlit application.

            Both components were containerized using **Docker** and deployed on **Google Cloud** (Cloud Run)

            """
)

st.markdown(
    """
            ## Going further 🚀
            There are many things that could be improved. Here are a few ideas:

            - Add **new data sources**, for example the reviews left about the Alan app in the play store.
            - Long reviews tend to be clustered wrongly, I could split them in small chunks
            - Build an Airflow pipeline to scrap new reviews and update the dashboard automatically
            - Spend more time fine tuning the hyper-parameters
    """
)
