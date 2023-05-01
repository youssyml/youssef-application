import streamlit as st
import datetime
import requests
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


PALETTE = [
    "rgb(93,88,244)",
    "rgb(51,227,158)",
    "rgb(227,50,68)",
    "rgb(255,184,225)",
    "rgb(206,212,218)",
]

st.title("Alan Google Maps reviews analysis dashboad")
st.markdown(
    """
    Review statistics about the reviews left on Alan on google maps and explore the main topics users talk about
    """
)


start_col, end_col = st.columns(2)
start = start_col.date_input("From", datetime.date(2022, 5, 1))
end = end_col.date_input("To", datetime.date(2023, 5, 1))

# get reviews
response = requests.get(
    url="http://localhost:8000/reviews",
    params={"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")},
).json()

reviews = pd.DataFrame(response.get("reviews"))

### BASIC STATISTICS ###
st.markdown(
    """
    ### Reviews and ratings overview 📊
    """
)

# compute statistics
n_reviews = len(reviews.text)
avg_rating = round(reviews.stars.mean(), 2)

review_col, rating_col = st.columns(2)
review_col.metric("Number of reviews", n_reviews)
rating_col.metric("Average rating", avg_rating)

# compute statistics by month
reviews["date"] = pd.to_datetime(reviews["date"])
reviews["yearmonth"] = reviews.date.dt.strftime("%Y-%m")
statistics = reviews.groupby("yearmonth", as_index=False).agg(
    {"stars": ["mean", "count"]}
)

statistics.columns = ["yearmonth", "avg_rating", "count"]

statistics.avg_rating = statistics.avg_rating.round(2)


fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_bar(
    x=statistics.yearmonth,
    y=statistics["count"],
    name="review count",
    marker=dict(color=PALETTE[0]),
)
fig1.add_trace(
    go.Scatter(
        x=statistics.yearmonth,
        y=statistics.avg_rating,
        name="average rating",
        mode="lines+markers",
        line=dict(color=PALETTE[1]),
        marker=dict(color=PALETTE[1]),
    ),
    secondary_y=True,
)
fig1.update_yaxes(title_text="review count", secondary_y=False)
fig1.update_yaxes(title_text="average rating", secondary_y=True, range=[0, 5])
st.plotly_chart(fig1)

### STRENGTH AND WEAKNESSES ###
st.markdown(
    """
    ### Strength and weaknesses 🚀
    Reviews are split into 2 groups : 1-2 star ratings (😢) and 4-5 star ratings (💪🏻).
    The most representative topics are then extracted from each group.
    """
)
response = requests.get(
    url="http://localhost:8000/reviews/sw",
    params={"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")},
).json()

strengths_col, improvements_col = st.columns(2)
strengths_col.markdown("**Strengths** 💪🏻")
improvements_col.markdown("**Improvement areas** 😢")
strengths_col.markdown("\n".join([f"- **{s}**" for s in response.get(("1"))]))
improvements_col.markdown("\n".join([f"- **{s}**" for s in response.get(("0"))]))


### REVIEW CLUSTERS ###
st.markdown(
    """
    ### Review clustering 👀
    Reviews are organised in clusters using their content. Reviews in gray are outliers.
    The main topics of each cluster are shown below.
    """
)

response = requests.get(
    url="http://localhost:8000/reviews/clusters",
    params={"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")},
).json()

scatter_df = pd.DataFrame(response.get("reviews"))

# truncate long reviews
scatter_df["truncated"] = scatter_df.text.map(
    lambda txt: "".join(
        [c + "-<br>" if (i + 1) % 50 == 0 else c for i, c in enumerate(txt)]
    )
)

fig2 = go.Figure(
    go.Scatter(
        x=scatter_df.x,
        y=scatter_df.y,
        mode="markers",
        hovertemplate="%{text}",
        text=scatter_df.truncated,
        showlegend=False,
        marker=dict(
            color=scatter_df.cluster.map(lambda c: PALETTE[c]),
        ),
    )
)

fig2.update_layout(showlegend=False)
fig2.update_traces(hovertemplate="%{text}<extra></extra>")
st.plotly_chart(fig2)


for i, cluster in enumerate(response.get("clusters")):
    if cluster != "-1":
        st.markdown(
            f"""
            <span style='color:{PALETTE[int(cluster)]}; font-weight:bold;'>Cluster {cluster}</span>:
            {" | ".join(list(response.get("clusters").get(cluster)))}
            """,
            unsafe_allow_html=True,
        )
