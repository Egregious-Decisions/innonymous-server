IMAGE=ghcr.io/egregious-decisions/innonymous-server

.PHONY: test
test:
	python -m pytest --testdox --cov=innonymous ./tests/


.PHONY: format
format:
	black ./innonymous/ && ruff --fix ./innonymous/
	black ./tests/ && ruff --fix ./tests/

.PHONY: lint
lint:
	black --check ./innonymous/ && ruff ./innonymous/ && mypy --install-types --non-interactive ./innonymous/
	black --check ./tests/ && ruff ./tests/ && mypy --install-types --non-interactive ./tests/


.PHONY: build
build:
	docker build -t ${IMAGE}:${TAG} .

.PHONY: push
push:
	docker push ${IMAGE}:${TAG}

.PHONY: pull
pull:
	docker pull ${IMAGE}:${TAG}

.PHONY: prune
prune:
	docker system prune -f
