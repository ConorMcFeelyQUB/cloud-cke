CLUSTER_NAME="cc-project-cluster"
PROJECT_ID="***"
ADVERT_IMAGE_NAME="gke-advert-i"
INDEXER_IMAGE_NAME="gke-indexer-i"
SEARCH_IMAGE_NAME="gke-search-i"

ZONE="europe-west2-a"

gcloud --quiet container clusters delete $CLUSTER_NAME --zone $ZONE

gcloud --quiet container images delete gcr.io/$PROJECT_ID/$ADVERT_IMAGE_NAME
gcloud --quiet container images delete gcr.io/$PROJECT_ID/$INDEXER_IMAGE_NAME
gcloud --quiet container images delete gcr.io/$PROJECT_ID/$SEARCH_IMAGE_NAME