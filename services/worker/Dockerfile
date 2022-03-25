FROM python:3.9

WORKDIR /app

COPY . .

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "celery", "-A", "services.worker.app", "worker", "-l", "info"]