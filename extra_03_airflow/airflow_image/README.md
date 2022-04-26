# Godeltech Airflow Docker Image
Docker container definition for Airflow instance

## Sources
Based on official Production Ready [Dockerfile](https://raw.githubusercontent.com/apache/airflow/v1-10-stable/Dockerfile) 
from stable branch of 1.10.x version 

Differences between "vanilla" Dockerfile and Godeltech Airflow Dockerfile

```shell script
diff --color <(curl https://raw.githubusercontent.com/apache/airflow/v1-10-stable/Dockerfile) Dockerfile
```

## Build Images
All building based on [Build Arguments](https://airflow.readthedocs.io/en/latest/production-deployment.html#id1)

### Additional Godeltech Airflow Build Arguments

| Build argument 	| Default value 	| Description 	|
|-------------------|-------------------|---------------|
| `PIP_INDEX_URL` 	| `https://pypi.org/simple` 	| Base URL of the Python Package Index	|
| `PIP_TRUSTED_HOST` 	|  	| Mark this host or host:port pair as trusted, even though it does not have valid or any HTTPS. |
| `PIP_EXTRA_INDEX_URL` 	|  	| Extra URLs of package indexes	|
| `PIP_DEFAULT_TIMEOUT` 	| `15` 	| Set the socket timeout |
| `ORACLE_INSTANCE_CLIENT_VERSION` 	| `19.5.0.0.0` 	| Oracle Instance Client Version |
| `ORACLE_HOME` 	| `/opt/oracle` 	| Installation directory for Oracle Instance Client	|
| `ADDITIONAL_GODELTECH_APT_DEPS` 	|  	|  Additional apt dev dependencies installed in the Godeltech Airflow image	|
| `ADDITIONAL_GODELTECH_PYTHON_DEPS` 	|  	| Additional python packages to extend the Godeltech Airflow image with some extra dependencies	|

### Local Build Image

Docker doesn't support build-args-file so we create helper to read build-args from file(s) and pass to docker build

#### For generate command run
```shell script
./docker_build_helper.py . -t godeltech-airflow --build-arg-file ./build.args
```

#### For generate and run command run
```shell script
eval $(./docker_build_helper.py . -t godeltech-airflow --build-arg-file ./build.args)
```

## Local run

You can configure your local Airflow, just change docker-compose.yml.example (see comments) and sample.env (see comments)

### Use latest image from ECR (do not forget to change profile for other accounts)
1. Copy `docker-compose.yml.example` to `docker-compose.yml`
2. Copy `sample.env` to `local.env`
3. Change configuration in docker-compose.yml:
   * `{{aws_account_id}}` replace to actual AWS Account ID
   * `{{airflow_name}}` replace to actual container image
4. Login to ECR registry
5. Pull latest images
6. Run

```shell script
$(aws ecr get-login --region eu-west-1 --no-include-email --profile data)
cp docker-compose.yml.example docker-compose.yml
cp sample.env local.env
docker-compose pull
docker-compose up
```

For terminate just press Ctrl+C (⌘ + C for Mac)

### Destroy containers
```shell script
docker-compose down
```
