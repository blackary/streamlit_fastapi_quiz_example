# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS

build: ## Build the container
	docker build -t quiz-img .
 
run: ## Run the container
	docker run -d --name quiz -p 80:80 quiz-img

up: build run ## Build and run container

stop: ## Stop and remove a running container
	docker stop quiz; docker rm quiz