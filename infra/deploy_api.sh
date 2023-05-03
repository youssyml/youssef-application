open -a docker
docker build -t $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_API:prod -f nlp/Dockerfile  .
docker push $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_API:prod
gcloud run deploy --image $GCR_DOMAIN/$GCP_PROJECT/$GCP_IMAGE_API:prod --memory 4Gi \
  --region $GCP_REGION
