gcloud compute addresses create test-service-default \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --description="test description" \
    --network=default


gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --ranges=test-service-default \
    --network=default \
    --project=cc-project-ke
