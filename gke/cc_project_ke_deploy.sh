set -ex

PROJECT_ID="fixing-index"
ADVERT_IMAGE_NAME="gke-advert-i"
INDEXER_IMAGE_NAME="gke-indexer-i"
SEARCH_IMAGE_NAME="gke-search-i"

ADVERT_DB_INSTANCE_NAME="advert-db-instance"
PAGE_DB_INSTANCE_NAME="page-db-instance"
DB_PASSWORD="QUBccProject"
REGION="europe-west2"
ZONE="europe-west2-a"
CLUSTER_NAME="cc-project-cluster"


gcloud beta container clusters create $CLUSTER_NAME \
    --zone $ZONE \
    --no-enable-basic-auth \
    --cluster-version "1.13.11-gke.14" \
    --machine-type "n1-standard-1" \
    --image-type "COS" --disk-type "pd-standard" \
    --disk-size "100" \
    --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
    --num-nodes "3" \
    --enable-stackdriver-kubernetes \
    --enable-ip-alias \
    --network "projects/fixing-index/global/networks/default" \
    --subnetwork "projects/fixing-index/regions/europe-west2/subnetworks/default" \
    --default-max-pods-per-node "110" \
    --addons HorizontalPodAutoscaling,HttpLoadBalancing \
    --enable-autoupgrade \
    --enable-autorepair


cd advert

gcloud builds submit --tag gcr.io/$PROJECT_ID/$ADVERT_IMAGE_NAME .

#deploy app
kubectl apply -f deployment.yaml

#register load balancer
kubectl apply -f service.yaml

cd ..

cd indexer

gcloud builds submit --tag gcr.io/$PROJECT_ID/$INDEXER_IMAGE_NAME . 

#deploy app
kubectl apply -f deployment.yaml

#register load balancer
kubectl apply -f service.yaml

cd ..

cd search
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SEARCH_IMAGE_NAME .

#deploy app
kubectl apply -f deployment.yaml

#register load balancer
kubectl apply -f service.yaml
