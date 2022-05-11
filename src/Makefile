SHELL=/bin/bash
# paths
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# defaults 
.DEFAULT_GOAL=help
count ?= 10

configure_env: compose_start tf_start generate python_env_setup
	
clean: tf_stop compose_stop clean_dirs
	
compose_start:
	cd infra && sudo docker-compose up -d

compose_stop: 
	cd infra && sudo docker-compose down

tf_start: 
	cd infra && terraform init && terraform apply --auto-approve

tf_stop: 
	cd infra && terraform destroy --auto-approve

generate:
	for i in {1..$(count)}; do $(ROOT_DIR)/../message-generators/linux ; done

clean_dirs:
	cd $(ROOT_DIR)/infra && find . -not -name '*tf' -not -name '*yml' -print0 | xargs -0 rm -rf -- 2> /dev/null || true
	cd $(ROOT_DIR)/tool && find . -not -name 'Dockerfile' -not -name '*py' -not -name '*txt' -print0 | xargs -0 rm -rf -- 2> /dev/null || true

python_env_setup:
	cd $(ROOT_DIR)/tool/ && virtualenv -p python3 venv && source venv/bin/activate && pip install -r requirements.txt
	@echo  ''
	@echo  'Tool is ready to use. Try:'
	@echo  '    source tool/venv/bin/activate'
	@echo  'then:'
	@echo  '    python tool/main_cli.py'
	@echo  ''

help:
	@echo  ''
	@echo  'Options:'
	@echo  '  make configure_env    - Configures docker compose, DynamoDB, SQS queue setup.'
	@echo  '                          Creates python virtualenv and install requirements for the tool.'
	@echo  '  make generate         - Creates SQS queue and generates 10 new messages'
	@echo  '  make generate count=n - Creates SQS queue and generates n new messages'
	@echo  '  make clean            - Removes generated configuration and log files' 
	@echo  ''
