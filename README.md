# Analyzing Alan's customer reviews on Google Maps

This repository contains the all the code needed to scrap and process reviews left on Alan's Google Maps business page.

## How to use me
### Environment variables
Make sure you copy the .env.sample, rename it to .env and fill it with your information.

### Useful make commands
In your terminal, you can run:
- make **install_scrapping** to install scrapping requirements
- make **install_nlp** to install nlp requirements
- make **install_streamlit** to install streamlit requirements
- make **scrap_data** to scrap the data from google maps
- make **process_scrapped_data** to parse the scrapped data
- make **run_local_nlp** to run the API locally
- make **run_local_app** to run the APP locally (make sure you set the API_URL env variable to point to the right API)
- make **deploy_nlp_api** to deploy the API on Google Cloud
- make **deploy_streamlit_app** to deploy the APP on Google Cloud



## Repository structure
- scrapping: code used to scrap and parse the data from Google Maps.
- nlp: code for the NLP API. Includes text preprocessing, analysis and API endpoints.
- streamlit: code for the streamlit dashboard
- infra: Shell scripts to deploy the project to GCP
