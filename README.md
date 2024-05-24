# CSCA 5028 Final Project: 🛰️ Sat Scan

**Sat Scan** helps users discover recently launched satellites and unidentified space objects.

To support this mission, the system periodically consumes data from a [Space-Track.org](https://www.space-track.org/auth/login) API to ingest, normalize, and maintain a database of recently launched satellites and other unidentified space objects. As the source and origin of recently discovered space objects is often unknown upon initial detection, Sat Scan's data collection process updates existing space object records with new information as it becomes available.

Sat Scan exposes the recently launched satellites and space objects to users via a web-based application. This client-facing application allows users to learn more about the origins of recently launched satellites, such as the country of origin and launch site.

> [!IMPORTANT]  
> This readme provides an overview of relevant development details. See this project's [Final Report](report/final-report.md) for an in-depth discussion of the project.

## Table of Contents

- [CSCA 5028 Final Project: 🛰️ Sat Scan](#csca-5028-final-project-️-sat-scan)
  - [Table of Contents](#table-of-contents)
  - [Project Rubric Requirements](#project-rubric-requirements)
  - [Project Structure](#project-structure)
  - [Local Development](#local-development)
    - [Initial Local Development Setup](#initial-local-development-setup)
    - [1. Create the necessary secret configuration files](#1-create-the-necessary-secret-configuration-files)
    - [2. Add you space-track.org username and password](#2-add-you-space-trackorg-username-and-password)
    - [3. Update the API Keys](#3-update-the-api-keys)
      - [Data Analyzer Example](#data-analyzer-example)
      - [API Example](#api-example)
    - [4. Prepare the database](#4-prepare-the-database)
    - [5. Run the Sat Scan backend system](#5-run-the-sat-scan-backend-system)
    - [6. Start the Frontend](#6-start-the-frontend)
  - [Continuous Integration](#continuous-integration)
    - [Linting - Code Formatting](#linting---code-formatting)
    - [Tests](#tests)
  - [Continuous Delivery](#continuous-delivery)
  - [Production Infrastructure](#production-infrastructure)
    - [Applying Terraform Changes](#applying-terraform-changes)
      - [1. Plan the change](#1-plan-the-change)
      - [2. Apply the change](#2-apply-the-change)
      - [3. Run the post-apply script](#3-run-the-post-apply-script)
      - [4. Generate a new task definition](#4-generate-a-new-task-definition)
      - [5. Generate a task definition](#5-generate-a-task-definition)
      - [6. Create a Pull Request with the Task-Definition Change](#6-create-a-pull-request-with-the-task-definition-change)
      - [Note: Creating an SSH Key](#note-creating-an-ssh-key)
  - [Database Migrations](#database-migrations)
    - [Local Database Migrations](#local-database-migrations)
    - [Production Database Migrations](#production-database-migrations)
      - [Notes on EC2 "JumpBox" Setup](#notes-on-ec2-jumpbox-setup)


## Project Rubric Requirements

Below is a table created based on the requirements published in CSCA5028's Week 1 "Project Rubric" reading.

| Requirement                                 | Present | Notes                                                                             | Reference                                                                                                                                                                                                                                                   |
|---------------------------------------------|---------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Web application, Report                     | ✅       | Next.js, Vercel                                                                   | [sat-scan-web](applications/sat-scan-web), [Report Ref](report/final-report.md#sat-scan-web)                                                                                                                                                                |
| Data collector                              | ✅       | Python, AWS Lambda                                                                | [space-data-collector](applications/space-data-collector), [Report Ref](report/final-report.md#data-collector)                                                                                                                                              |
| Data analyzer                               | ✅       | Python, AWS ECS                                                                   | [space-data-analyzer](applications/space-data-analyzer), [Report Ref](report/final-report.md#data-analyzer)                                                                                                                                                 |
| Unit test                                   | ✅       | All Apps                                                                          | [sat-scan-web] `yarn test` [data collector, analyzer, and API] `make unit`                                                                                                                                                                                  |
| Data persistence                            | ✅       | Local Development & Production                                                    | [docker-compose.yml](docker-compose.yml), [infrastructure/main.tf](/infrastructure/main.tf)                                                                                                                                                                 |
| Rest collaboration internal or API endpoint | ✅       | Dedicated API, internally and publicly accessible                                 | [sat-scan-api](applications/sat-scan-api)                                                                                                                                                                                                                   |
| Product environment                         | ✅       | Terraform, AWS & Vercel via Continuous Deployment                                 | [infrastructure/main.tf](/infrastructure/main.tf)                                                                                                                                                                                                           |
| Integration tests                           | ✅       | API & Database interaction, dockerized, runs during continuous integration checks | From root directory: `make integration`                                                                                                                                                                                                                      |
| Using mock objects or any test doubles      | ✅       | Used as needed throughout tests                                                   | [spy](applications/sat-scan-web/src/interfaces/spaceObject/test.ts), [object mock](applications/sat-scan-web/src/test/mocks/generateRawMockSpaceObject.ts), [interface mock](applications/space-data-collector/test/test_rabbit_mq_connection_interface.py) |
| Continuous integration                      | ✅       | GitHub Actions to lint & test                                                     | [GitHub Action Workflows](.github/workflows)                                                                                                                                                                                                           |
| Production monitoring                       | ✅       | AWS CloudWatch                                                                    | [Report Ref](report/final-report.md#production-monitoring)                                                                                                                                                                                                  |
| Event collaboration messaging               | ✅       | Local Development & Production                                                    | [docker-compose.yml](docker-compose.yml), [infrastructure/main.tf](/infrastructure/main.tf)                                                                                                                                                                 |
| Continuous delivery                         | ✅       | GitHub Actions, deployed to AWS & Vercel                                          | [GitHub Action Workflows](.github/workflows)                                                                                                                                                                                                           |


## Project Structure

This project contains multiple applications in a "monorepo" structure.

```
├── applications
│   ├── sat-scan-api
│   ├── sat-scan-web
│   ├── space-data-analyzer
│   └── space-data-collector
├── databases
├── infrastructure
│   ├── database-migrations
│   └── task-definitions
└── test
    └── sat_scan_api
        └── integration
```

All of the "applications" are grouped within the `/applications` directory. 

The `/infrastructure` directory contains all of the Terraform code to provision the production environment. It also contains the post-provisioning scripts to setup the database and publish production routing configurations. 

Database migrations are located within the `/databases` directory.

While application level unit tests can be found within their respective `/application/*` directories, integration tests are located within the `/test` directory.

## Local Development

The `docker-compose.yml` file located at the project's root allows for the entire backend Sat System to be ran locally. The Data Collector, Data Analzyer, and Sat Scan API dockerfiles can be found in their respective directory, within `/applications`.

Local Next.js application development doesn't require (nor considerably benefit from) running within a Docker container. As such, local development instructions for the Web application can found within the app's `README.md`.

### Initial Local Development Setup

### 1. Create the necessary secret configuration files

Each of the backend applications uses `credentials.ini` files to inject sensitive local and production environment variables. These `credentials.ini` files in the `.gitignore` file, which prevents them from being committed.

Use the `example.credentials.ini` files in each application directory as the basis to create local `credentials.ini` files.

- [Data Collector](applications/space-data-collector/example.credentials.ini)
- [Data Analyzer](applications/space-data-analyzer/example.credentials.ini)
- [Sat Scan API](applications/sat-scan-api/example.credentials.ini)

### 2. Add you space-track.org username and password

Create an account on [Space-Track.org](https://www.space-track.org/auth/login) to use the [Space-Track.org API](https://www.space-track.org/documentation#/api) during local development. 

Once done, add these values to your [applications/space-data-collector/credentials.ini](applications/space-data-collector/credentials.ini) file.

### 3. Update the API Keys

The Sat Scan API uses an API key that is passed as a bearer token to authenticate requests to create, update, or destroy resources. As the Data Analyzer communicates with the API to create and update space object records, both the Data Analyzer and API need to specify a shared machine-to-machine API key in their `credentials.ini` files. For local development, this api key can be any string value.


#### [Data Analyzer](applications/space-data-analyzer/credentials.ini) Example

```
[sat-scan-api]
key = local_development_key
```

#### [API](applications/sat-scan-api/credentials.ini) Example

```
[api-keys]
keys = local_development_key
```

### 4. Prepare the database

This project uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage migrations. To apply the migrations, start the local database and apply the schema changes.

From the root directory, start the docker database:

```
docker-compose up database
```

Create a virtual Python environment,

```
python3 -m venv .venv && source .venv/bin/activate
```

Install the project Python dependencies,

```
pip3 install -r requirements.txt
```

Then, apply the database migrations:

```
alembic upgrade head
```

### 5. Run the Sat Scan backend system

Docker Compose is used to run all of Sat Scan's backend applications and services locally. You can start it by running the following command from the root directory. 

> [!WARNING]  
> The Data Collector application will begin periodically fetching data from the Space-Track.org API once started

```
docker-compose up --build
```

### 6. Start the Frontend

Navigate to the Sat Scan Web directory, install the dependencies, and start the development environment.

```
cd applications/sat-scan-web
yarn
yarn dev
```

## Continuous Integration

Continuous integration checks are ran using GitHub Actions. The following CI checks currently exist:

| Continuous Integration Check | Link                                                             |
|------------------------------|------------------------------------------------------------------|
| Linting                      | [lint.yml](.github/workflows/lint.yml)                           |
| Unit Tests                   | [unit_tests.yml](.github/workflows/unit_tests.yml)               |
| Integration Tests            | [integration_tests.yml](.github/workflows/integration_tests.yml) |

### Linting - Code Formatting

Run `make format` to format the Python code locally. 

To format [sat-scan-web](applications/sat-scan-web/), `cd` into the application directory, run `yarn`, and the run `yarn format`.

### Tests

Unit tests are located in their respective `/applications/*` directory.

Integration tests can be ran from the root directory using `make integration`.

## Continuous Delivery

> [!TIP]  
> Additional information about continuous delivery for each application and service be found in the project's [report documentation](report/final-report.md)

Each application is automatically deployed to a production environment when a new pull request is merged into the `main` development branch.

Each backend application has a unique GitHub action to facilitate deployment to the appropriate production environment.

Sat Scan Web, the frontend application, is hosted on Vercel. "Preview deployments" are created by Vercel each time a new commit is pushed to an open pull request. Like the backend continuous deployments, Vercel deploys the app to production when new commits are pushed/merged to `main`.

| Continuous Delivery Pipelines | Link                                                                     |
|-------------------------------|--------------------------------------------------------------------------|
| API                           | [lint.yml](.github/workflows/api_deploy.yml)                             |
| Data Analyzer                 | [unit_tests.yml](.github/workflows/data_analyzer_deploy.yml)             |
| Data Collector                | [integration_tests.yml](.github/workflows/data_collector_deployment.yml) |

## Production Infrastructure

All of the production backend infrastructure is provisioned using Terraform, which can be found in the `/infrastructure` directory.

### Applying Terraform Changes

To make changes to the production infrastructure, `cd` into the `/infrastructure` directory.

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

#### 5. Generate a task definition

After applying the, new task definitions can be generated using the following commands (run from root project directory):

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

#### 6. Create a Pull Request with the Task-Definition Change

When the continuous integration checks pass, merge the pull request into the `main` branch. Merging into main will trigger the continuous deployment pipeline, which builds a new image, pushes it to ECR, and deploys the image to ECS.

#### Note: Creating an SSH Key

The following command can be used to regenerated an SSH key:

```
ssh-keygen -t rsa -b 4096 -m pem -f sat_scan_kp && openssl rsa -in sat_scan_kp -outform pem && chmod 400 sat_scan_kp.pem
```

## Database Migrations

### Local Database Migrations

Local database migrations and rollbacks can be managed using `alembic upgrade head` and `alembic downgrade -1`

### Production Database Migrations

Production database migrations are applied using the [post_apply.sh](/infrastructure/post_apply.sh) script.

The `post_apply.sh` script handles SSHing into the EC2 instance to run the database migrations using alembic.

#### Notes on EC2 "JumpBox" Setup

This project currently uses an AWS EC2 instance to manually apply database migration changes. A more mature system should apply database migrations alongside deployments, with the ability to rollback the migration should the deploy fail.

Using an EC2 allows for a better security posture by restricting database access to within the VPC and only allowing SSH ingress from a local IP address. As this EC2 exists within the VPC, it can communicate with the RDS instance and apply schema changes.

This represents an incremental step towards DB migration automation, as these steps can be migrated to a GitHub Action or alternative workflow as time allows.