# CSCA 5028 Final Project: Sat Scan

**Sat Scan** displays the location of recently launched satellites. 

## Project Requirements

In Progress:

- Production monitoring instrumenting
  - Prometheus & Grafana

Later:

- Web application basic form, reporting

~Done:

- ~~Product environment~~ 5/15
- ~~Continuous integration~~ 5/15
- ~~Unit tests~~ 5/15
- ~~Integration tests~~ 5/15
- ~~- Continuous delivery~~ 5/6 mvp
- ~~- Data analyzer~~ 5/2 mvp
- ~~Data collection~~ 4/30 mvp
- ~~Event collaboration messaging~~ 4/30 mvp
- ~~Data persistence any data store~~ 5/1 mvp
- ~~Rest collaboration internal or API endpoint~~ 5/1 mvp

## Notes

### Code Formatting

Run `black **/*.py` to format all Python files

#### To run existing migrations

```
alembic upgrade head
```

#### To reverse migration

```
alembic downgrade -1
```


### Terraform

To make a terraform change:

*Run each command from within the `/infrastructure` directory


#### 1. Plan the change


```
terraform plan -var-file="secrets.tfvars"
```

#### 2. Apply the change


```
terraform apply -var-file="secrets.tfvars"
```

#### 3. Run the post-apply script

This pushes route configuration information for the provisioned infrastructure to a config.ini file in an S3 bucket. The continuous deployment pipeline injects this configuration into the application when create the build artifact.

```
./post_apply.sh
```

#### 4. Generate a new task definition

Then output endpoints to file used by ci/cd

#### Generate a task definition

Run after plan

```
aws ecs describe-task-definition \
   --task-definition sat-scan-api-family \
   --query taskDefinition > infrastructure/task-definitions/aws/sat-scan-api-container.json
```

```
aws ecs describe-task-definition \
   --task-definition data-analyzer-family \
   --query taskDefinition > infrastructure/task-definitions/aws/data-analyzer-container.json
```

#### 5. Create a Pull Request with the Task-Definition Change

When the continuous integration checks pass, merge the pull request into the `main` branch. Merging into main will trigger the continuous deployment pipeline, which builds a new image, pushes it to ECR, and deploys the image to ECS.

### Terraform Notes

#### Creating an SSH Key

Consider the following if you need to create an SSH key

```
ssh-keygen -t rsa -b 4096 -m pem -f sat_scan_kp && openssl rsa -in sat_scan_kp -outform pem && chmod 400 sat_scan_kp.pem
```

## Database Migration

### EC2 Setup

Currently using an EC2 instance to manually apply database migration changes. A more mature system should apply database migrations alongside deployments, with the ability to rollback the migration should the deploy fail.

For now, we'll maintain the system's security posture by continuing to restrict database access to within the VPC. We'll create an EC2 instance that only allows ingress SSH traffic from a local IP address. As this EC2 exists within the VPC, it can communicate with the RDS instance and apply schema changes.

This represents an incremental step towards DB migration automation, as these steps can be migrated to a GitHub Action or alternative workflow as time allows.

#### Copy Migrations to EC2 instance

SSH into the EC2 and run `mkdir database-migration`

Move the relevant migration files onto the EC2:

```
scp -r -i infrastructure/sat_scan_kp.pem alembic.ini ubuntu@ec2-18-223-42-178.us-east-2.compute.amazonaws.com:~/database-migration
scp -r -i infrastructure/sat_scan_kp.pem ./databases ubuntu@ec2-18-223-42-178.us-east-2.compute.amazonaws.com:~/database-migration
```

Connect to EC2 instance:

```
ssh -i "infrastructure/sat_scan_kp.pem" ubuntu@ec2-18-223-42-178.us-east-2.compute.amazonaws.com
```

Install python and deps:

```
sudo apt-get update
sudo apt install python3-pip \
   python3.8-venv \
   libpq-dev



python3 -m venv .venv && source .venv/bin/activate

pip3 install alembic psycopg2 
```

Then, edit the `alembic.ini` file to use the RDS connection string.

Finally, apply the migrations:

```
alembic upgrade head
```