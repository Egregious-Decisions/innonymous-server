IMAGE=smthngslv/innonymous-api-server

test:
	python -m pytest --testdox --cov=innonymous ./tests/


format:
	black ./innonymous/ && ruff --fix ./innonymous/
	black ./tests/ && ruff --fix ./tests/

lint:
	black --check ./innonymous/ && ruff ./innonymous/ && mypy --install-types --non-interactive ./innonymous/
	black --check ./tests/ && ruff ./tests/ && mypy --install-types --non-interactive ./tests/


build:
	docker build -t ${IMAGE}:${TAG} .

push:
	docker push ${IMAGE}:${TAG}

pull:
	docker pull ${IMAGE}:${TAG}

prune:
	docker system prune -f
