FROM python:3.10-slim

# Actually, we do not need root.
RUN groupadd idiots && useradd animenerd1337 -g idiots

# Locale.
ENV LANG en_US.utf8
RUN apt-get update -y && apt-get install -y locales alien && \
    localedef -i en_US -c -f UTF-8 -A \/usr/share/locale/locale.alias en_US.UTF-8

# Environment.
WORKDIR /app
COPY ./poetry.lock ./
COPY ./pyproject.toml ./
RUN pip install --no-cache-dir --upgrade --root-user-action ignore pip setuptools wheel poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# App.
COPY ./src ./src
RUN poetry install

USER animenerd1337
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "innonymous:app"]
