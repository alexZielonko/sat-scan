#!/bin/bash

###########################################################
# Script Name: post_apply.sh
# Description: 
# - Run after applying terraform changes
# - Creates route-config.ini file for downstream application 
#   useage during continuous integration and   deployment pipelines
# - Runs database migrations
###########################################################

# Create and upload route-config.ini file to S3

echo "👉 Creating route-config.ini file"

S3_BUCKET_URI="s3://sat-scan-route-config"
OUTPUT_FILE_NAME="route-config.ini"

load_balancer=`terraform output -json | jq -r ".load_balancer_ip.value"`
database_endpoint=`terraform output -json | jq -r ".database_endpoint.value.endpoint"`

mq_broker_username=`terraform output -json | jq -r ".mq_broker_user.value.username"`
mq_broker_password=`terraform output -json | jq -r ".mq_broker_user.value.password"`
mq_broker_broker_id=`terraform output -json | jq -r ".mq_broker.value[0].id"`

sat_scan_api_base_url="http://${load_balancer}"

echo "$sat_scan_api_base_url"

cat <<EOF > $OUTPUT_FILE_NAME
[sat-scan-api]
base_url=$sat_scan_api_base_url

[database]
env=PROD
database_endpoint=$database_endpoint
database_name=sat_scan_db

[mq_broker]
env=PROD
rabbitmq_user=$mq_broker_username
rabbitmq_password=$mq_broker_password
rabbitmq_broker_id=$mq_broker_broker_id
rabbitmq_region=us-east-2
EOF

echo "Created temporary "$OUTPUT_FILE_NAME" file"

aws s3 cp $OUTPUT_FILE_NAME $S3_BUCKET_URI

echo "Deleted "$OUTPUT_FILE_NAME" file"

rm $OUTPUT_FILE_NAME

# Apply database migrations to RDS

echo "👉 Running database migrations"

ec2_dns=`terraform output -json | jq -r ".ec2_dns.value"`

MIGRATION_DIRECTORY=database-migrations

ssh -i "sat_scan_kp.pem" ubuntu@$ec2_dns << EOF
  rm -rf $MIGRATION_DIRECTORY
  mkdir $MIGRATION_DIRECTORY
  exit
EOF

db_name=`terraform output -json | jq -r ".database_endpoint.value.db_name"`
db_user=`terraform output -json | jq -r ".database_endpoint.value.username"`
db_pass=`terraform output -json | jq -r ".database_endpoint.value.password"`

db_connection_url="postgresql://${db_user}:${db_pass}@${database_endpoint}/${db_name}"

cat <<EOF > alembic.ini
  [alembic]
  script_location = databases
  version_path_separator = os
  sqlalchemy.url = ${db_connection_url}
  [loggers]
  keys = root,sqlalchemy,alembic
  [handlers]
  keys = console
  [formatters]
  keys = generic
  [logger_root]
  level = WARN
  handlers = console
  qualname =
  [logger_sqlalchemy]
  level = WARN
  handlers =
  qualname = sqlalchemy.engine
  [logger_alembic]
  level = INFO
  handlers =
  qualname = alembic
  [handler_console]
  class = StreamHandler
  args = (sys.stderr,)
  level = NOTSET
  formatter = generic
  [formatter_generic]
  format = %(levelname)-5.5s [%(name)s] %(message)s
  datefmt = %H:%M:%S
EOF

echo "-------------------------------------"
echo "⏳ Transfering migration files to EC2"
echo "-------------------------------------"

scp -r -i sat_scan_kp.pem alembic.ini ubuntu@$ec2_dns:~/$MIGRATION_DIRECTORY
scp -r -i sat_scan_kp.pem ../databases ubuntu@$ec2_dns:~/$MIGRATION_DIRECTORY

rm alembic.ini

echo "-------------------------------------"
echo "⏳ Provisioning EC2 instance & Applying Migrations"
echo "-------------------------------------"

ssh -i "sat_scan_kp.pem" ubuntu@$ec2_dns << EOF
  sudo apt-get update
  sudo apt install -y python3-pip \
    python3.8-venv \
    libpq-dev
  python3 -m venv .venv && source .venv/bin/activate
  cd $MIGRATION_DIRECTORY
  python3 -m venv .venv && source .venv/bin/activate
  pip3 install alembic psycopg2 
  alembic upgrade head
  exit
EOF
