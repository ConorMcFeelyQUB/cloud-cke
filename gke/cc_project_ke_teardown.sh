CLUSTER_NAME="cc-project-cluster"
PROJECT_ID="fixing-index"
ADVERT_IMAGE_NAME="gke-advert-i"
INDEXER_IMAGE_NAME="gke-indexer-i"
SEARCH_IMAGE_NAME="gke-search-i"

gcloud container clusters delete $CLUSTER_NAME

gcloud container images delete gcr.io/$PROJECT_ID/$ADVERT_IMAGE_NAME
gcloud container images delete gcr.io/$PROJECT_ID/$INDEXER_IMAGE_NAME
gcloud container images delete gcr.io/$PROJECT_ID/$SEARCH_IMAGE_NAME