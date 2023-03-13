# Innonymous API Server

A lightweight and fast API Server for anonymous chat.

## Environment

The project requires **Python 3.10** or newer.

The best way is to use `conda` or `venv`.

```shell
python -m venv myenv
conda create -n myenv python=3.10
```

The next step is install poetry (do not forget to activate your virtual environment first).

```shell
pip install poetry
poetry install
pip list  # Check if you current environment has all dependencies. 
```

## Makefile

You'll need to install `make` to work with `Makefile`.

You can run any of the following commands from the root directory of the project.

* `make format` - Apply formatting rules. Make sure to run before committing.
* `make lint` - Analyzes source code without changes. Make sure to use before committing.
* `make test` - Run tests. You need running docker for this command.
* `make prune` - Clear docker cache.
* `TAG=<mytag> make build` - Build a docker image with a given tag.
* `TAG=<mytag> make pull` - Pull a docker image with a given tag.
* `TAG=<mytag> make push` - Push a docker image with a given tag.
