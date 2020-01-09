set -ex

ADVERT_DB_INSTANCE_NAME="advert-db-instance"
PAGE_DB_INSTANCE_NAME="page-db-instance"
DB_PASSWORD="QUBccProject"
REGION="europe-west2"
ZONE="europe-west2-a"

STATIC_IP_SQL_SETUP_INSTANCE="static-sql-setup"
SQL_SETUP_INSTANCE_NAME="sql-setup-vm-instance"

#delete advert sql instance
gcloud --quiet sql instances delete $ADVERT_DB_INSTANCE_NAME

#delete page sql instance
gcloud --quiet sql instances delete $PAGE_DB_INSTANCE_NAME


#delete sql vm instance
gcloud --quiet compute instances delete $SQL_SETUP_INSTANCE_NAME \
    --zone=$ZONE --delete-disks=all

#delete static ip for vm instnace
gcloud --quiet compute addresses delete $STATIC_IP_SQL_SETUP_INSTANCE \
    --region $REGION
