##### PACKAGE INSTALLATION #####
install_scrapping:
	@pip install -r scrapping/requirements.txt

install_nlp:
	@pip install -r nlp/requirements.txt

install_streamlit:
	@pip install -r streamlit/requirements.txt

##### SCRAPPING #####
scrap_data:
	@mkdir data
	@python scrapping/scrapping.py

process_scrapped_data:
	@python scrapping/processing.py

##### RUN PROJECT LOCALLY #####
run_local_nlp:
	@uvicorn nlp.fast:app --reload

run_local_app:
	@streamlit run streamlit/Alan_reviews_👀.py

##### DEPLOY ON GOOGLE CLOUD #####
deploy_nlp_api:
	@sh infra/deploy_api.sh

deploy_streamlit_app:
	@sh infra/deploy_app.sh
