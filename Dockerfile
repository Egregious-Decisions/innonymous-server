FROM python:3.10-alpine

RUN addgroup -S idiots && adduser -S animenerd1337 -g idiots

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r ./requirements.txt && \
    rm ./requirements.txt

COPY ./innonymous ./innonymous

USER animenerd1337
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "innonymous:app"]
