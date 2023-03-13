## Environment

The best way is to use `conda` or `venv`.
```shell
python -m venv myenv # Use python 3.10 only.
conda create -n myenv python=3.10
```

The next step is install poetry (do not forget to activate your virtual environment first).
```shell
pip install poetry
poetry install
pip list  # Check if you current environment has all dependencies. 
```

## Makefile

To be able to work with Makefile, you need install make.
```shell
brew install make  # MacOS
apt/apt-get install make  # Linux.
```

There are several commands, that can help you during development. You should be in project root directory to use them.
* `make format` - Apply formatting rules for `.src` directory. Use it before committing to git.
* `make lint` - This command just validates files in `.src` directory, no files should be changed.  Use it before 
committing to git.
* `make test` - Run some tests. You need running docker for this command.
* `make prune` - Clear docker cache.
* `TAG=mytag make build` - Build docker image with given tag.
* `TAG=mytag make pull` - Pull docker image with given tag.
* `TAG=mytag make push` - Push docker image with given tag.
