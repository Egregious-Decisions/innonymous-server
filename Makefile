###--VARIABLES--########################################################################################################

IMAGE=smthngslv/innonymous-api-server

########################################################################################################################

###--TEST--#############################################################################################################

test:
	cd ./src/ && python -m pytest --testdox --cov=innonymous ./tests/

########################################################################################################################

###--LINT--#############################################################################################################

format:
	black ./src/ && ruff --fix ./src/innonymous/

lint:
	black --check ./src/ && ruff ./src/innonymous && mypy --install-types --non-interactive ./src/innonymous/

########################################################################################################################

###--DOCKER--###########################################################################################################

build:
	docker build -t ${IMAGE}:${TAG} .

push:
	docker push ${IMAGE}:${TAG}

pull:
	docker pull ${IMAGE}:${TAG}

prune:
	docker system prune -f

########################################################################################################################
