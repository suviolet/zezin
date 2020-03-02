
PROJECT_NAME = zezin
UID = $$(id -u)
GID = $$(id -g)

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".cache" -type d | xargs rm -rf
	@find . -name ".coverage" -type f | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@echo 'Temporary files deleted'

requirements-pip:  ## Install the app requirements
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

init_db:  ## Start alembic with new DB
	python -m zezin.manage db init

migrate:  ## Create migrations
	python -m zezin.manage db migrate

upgrade: ## Execute the migrations
	python -m zezin.manage db upgrade

lint: clean  ## Run pylint linter
	@printf '\n --- \n >>> Running linter...<<<\n'
	@pylint $(PROJECT_NAME)/*
	@printf '\n FINISHED! \n --- \n'

style:  ## Run isort and black auto formatting code style in the project
	@isort -m 3 -tc -y
	@black -S -t py37 -l 79 $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|venv|build|dist)/'

style-check:  ## Check isort and black code style
	@black -S -t py37 -l 79 --check $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|venv|build|dist)/'

runserver-dev: clean migrate  ## Run dev (flask) web server
	export FLASK_APP=$(PROJECT_NAME).app.py && flask run

docker-compose-up: clean ## Up docker-compose for development
	@docker-compose up -d

docker-compose-stop: clean ## Stop docker-compose for development
	@docker-compose stop

docker-compose-rm: docker-compose-stop  ## Delete the development environment containers
	@docker-compose rm -f