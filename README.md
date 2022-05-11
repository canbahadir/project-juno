# SQS to DynamoDB Processor

## Overview 

This tool consumes SQS messages from given or default endpoint and stores them on DynamoDB at same endpoint, also can clear DynamoDB table if needed. 

## Tool Requirements

- python (Python 3.6 up to 3.9 supported)
- pip (Python package manager)

## Installing

Currently the tool uses venv to work. To make the tool ready to use, run:

```bash
cd src/tool/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure Environment

This tool is tested with localstack. Follow these steps to create a working environment for tool:

Setup environment requirements:

- [docker](https://www.docker.com/get-started)
- [docker-compose](https://docs.docker.com/compose/install/)
- [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started)

### Using Makefile
Go to src directory and run:

```bash
cd src
make configure_env
```

To remove environment
```bash
cd src
make clean
```

### Manually
Setup localstack:

```bash
cd src/infra
docker-compose up
```

Setup DynamoDB on localstack:

```bash
cd src/infra
terraform init
terraform apply -auto-approve
```

Setup SQS on localstack with 1 query:

```bash
$ ./message-generators/linux    # for linux
$ ./message-generators/darwin   # for macos
```

Running this command multiple times creates additional queries.

## Running

This tool can be used by just using following command. Upon entering command the tool will show possible options. 

```bash
cd src/tool/
python main_cli.py
```

## Usage
This tool supports following parameters 

- `consume --count n`: Consume `n` messages
    Prints `n` consumed messages with message content and `MessageId`s from SQS context
    **e.g.: python main_cli.py consume --count 3**
- `show`: Show all consumed messages
    Prints all consumed messages with message content and `MessageId`s from SQS context
    **e.g.: python main_cli.py show**
- `clear`: Clear all consumed messages from database
    **e.g.: python main_cli.py clear**

This tool also supports following environmental variables

- AWS_REGION              / default=ap-southeast-1
- SQS_and_DB_ENDPOINT     / default=http://localhost:4576
- USE_SSL                 / default=True
- ACCESS_KEY              / default=mock
- SECRET_KEY              / default=mock
- SQS_QUEUE_NAME          / default=test-queue

These variables can be combined partially or all together with tool commands do configure tool further.

e.g:

```bash
AWS_REGION=ap-southeast-1 SQS_and_DB_ENDPOINT=http://localhost:4576 USE_SSL=0 ACCESS_KEY=mock SECRET_KEY=mock SQS_QUEUE_NAME=test-queue python main_cli.py show
```
### Usage with Docker

Create a docker container for tool:

```bash
cd src/tool/
docker build --tag <container_tag> .
```
To use tool with Container you need to use docker environments. Two env defined for usage:

- CMD    // can be used with consume|show|clear
- COUNT  // can be used with --count n

Example commands:
```bash
sudo docker run  -e CMD='consume' -e COUNT='--count 3' --network="host" cli-docker
sudo docker run  -e CMD='show' --network="host" cli-docker
sudo docker run  -e CMD='clear' --network="host" cli-docker
```
*--network="host" needed for coker to access localhost.*


## Challenges while solving the problem

- Learned SQS usage
- Learned DynamoDB usage
- Learned AWS user/service account creation with limited access
- Learned localstack configuration/usage
- Learned boto3,fire python library&package usage
- Learned how to pass conditional argument in python

## Notes

- I used Python 3 for developing this program because there is a good amount of support for AWS-Python3 integration and this is the language I am most fiamiliar out of the listed 4.
- Used DynamoDB because localstack has already support for DynamoDB and it looked like it is easier to deploy among other options. Also it is part of AWS ecosystem.


## Architecture and To-Do

```
$ tree .
├── DOCUMENTATION.md             // Mostly done.
├── ANSWERS.md                   // Done.
└── src
    └── infra
        └── ddbconf.tf           // Done.
        └── docker-compose.yml   // Done.
        └── main.tf              // Done.
        tool
        └── main_cli.py          // Logic done. Improvements needed.
        └── requirements.txt     // Done.
        └── Dockerfile           // Done.
    └── Makefile                 // Done.
└── message-generators
    └── darwin                   // default
    └── linux                    // default
    └── windows.exe              // default
├── docker-compose.yml           // default
├── README.md                    // default
├── .gitignore                   // Done.
```

- [X] Make tool runnable by docker.
- [X] Prepare a Makefile that creates environment.