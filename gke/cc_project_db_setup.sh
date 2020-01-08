set -ex

ADVERT_DB_INSTANCE_NAME="advert-db-instance"
PAGE_DB_INSTANCE_NAME="page-db-instance"
DB_PASSWORD="QUBccProject"
REGION="europe-west2"
ZONE="europe-west2-a"

#CREATE advert and PAge sql instances

gcloud beta sql instances create $ADVERT_DB_INSTANCE_NAME \
    --tier="db-n1-standard-2" \
    --region="europe-west2" \
    --network="default"

gcloud beta sql instances create $PAGE_DB_INSTANCE_NAME \
    --tier="db-n1-standard-2" \
    --region="europe-west2" \
    --network="default"

gcloud sql users set-password root --host=% --instance $ADVERT_DB_INSTANCE_NAME --password $DB_PASSWORD

gcloud sql users set-password root --host=% --instance $PAGE_DB_INSTANCE_NAME --password $DB_PASSWORD

gcloud services enable sqladmin.googleapis.com

############################################################
#Creating db tables and putting initial data

STATIC_IP_SQL_SETUP_INSTANCE="static-sql-setup"

#Creating a static IP for the sqlsetup vm
gcloud compute addresses create $STATIC_IP_SQL_SETUP_INSTANCE \
    --region $REGION \

#Storing the newly created static ip 
STATIC_IP_SQL_SETUP="$(gcloud compute addresses describe $STATIC_IP_SQL_SETUP_INSTANCE --region $REGION --format='get(address)')"


#Add setup IP to authorised list for advert sql instance
gcloud --quiet sql instances patch $ADVERT_DB_INSTANCE_NAME --authorized-networks="${STATIC_IP_SQL_SETUP}",

#Add setup IP to authorised list for page sql instance
gcloud --quiet sql instances patch $PAGE_DB_INSTANCE_NAME --authorized-networks="${STATIC_IP_SQL_SETUP}",

#create vm instance to run mysql commands

SQL_SETUP_INSTANCE_NAME="sql-setup-vm-instance"

gcloud compute instances create $SQL_SETUP_INSTANCE_NAME \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=g1-small \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=startup-script-sql-setup.sh \
    --zone $ZONE \
    --tags http-server \
    --address ${STATIC_IP_SQL_SETUP}



################################