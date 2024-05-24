# CSCA 5028 Final Project: 🛰️ Sat Scan

**Sat Scan** helps users discover recently launched satellites and unidentified space objects.

## Project Rubric Requirements

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

## Continuous Integration

### Linting

#### Code Formatting

Run `make format` to format the Python code locally. 

To format [sat-scan-web](applications/sat-scan-web/), `cd` into the application directory, run `yarn`, and the run `yarn format`.

### Tests

Unit tests are located in their respective `/applications/*` directory.

Integration tests can be ran from the root directory using `make integration`.

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