#!/bin/bash

###########################################################
# Script Name: post_apply.sh
# Description: Uploads endpoints and urls of infrastructure
#  provisioned by Terraform for injection into application 
#  code during continuous deployment process
###########################################################

S3_BUCKET_URI="s3://sat-scan-route-config"
OUTPUT_FILE_NAME="route-config.ini"

load_balancer=`terraform output -json | jq -r ".load_balancer_ip.value"`
database_endpoint=`terraform output -json | jq -r ".database_endpoint.value.endpoint"`
database_port=`terraform output -json | jq -r ".database_endpoint.value.port"`

cat <<EOF > $OUTPUT_FILE_NAME
[load_balancer]
load_balancer=$load_balancer

[database]
database_endpoint=$database_endpoint
database_port=$database_port
database_name=sat_scan_db
env=PROD
EOF

echo "Created temporary "$OUTPUT_FILE_NAME" file"

aws s3 cp $OUTPUT_FILE_NAME $S3_BUCKET_URI

echo "Deleted "$OUTPUT_FILE_NAME" file"

rm $OUTPUT_FILE_NAME