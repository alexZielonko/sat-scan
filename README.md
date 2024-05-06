# CSCA 5028 Final Project: Sat Scan

**Sat Scan** displays the location of recently launched satellites. 

## Project Requirements

In Progress:

- Product environment
- Continuous integration


Later:

- Web application basic form, reporting
- Unit tests
- Integration tests
- Using mock objects or any test doubles
- Production monitoring instrumenting

~Done:

- ~~- Continuous delivery~~ 5/6 mvp
- ~~- Data analyzer~~ 5/2 mvp
- ~~Data collection~~ 4/30 mvp
- ~~Event collaboration messaging~~ 4/30 mvp
- ~~Data persistence any data store~~ 5/1 mvp
- ~~Rest collaboration internal or API endpoint~~ 5/1 mvp

## Notes

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

#### 5. Create a Pull Request with the Task-Definition Change

When the continuous integration checks pass, merge the pull request into the `main` branch. Merging into main will trigger the continuous deployment pipeline, which builds a new image, pushes it to ECR, and deploys the image to ECS.

### Terraform Notes

#### Creating an SSH Key

Consider the following if you need to create an SSH key

```
ssh-keygen -t rsa -b 4096 -m pem -f sat_scan_kp && openssl rsa -in sat_scan_kp -outform pem && chmod 400 sat_scan_kp.pem
```