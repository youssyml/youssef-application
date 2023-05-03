open -a docker
docker build -t $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_APP:prod -f streamlit/Dockerfile  .
docker push $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_APP:prod
gcloud run deploy --image $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_APP:prod --memory 2Gi \
  --region $GCP_REGION --set-env-vars API_URL=$API_URL
