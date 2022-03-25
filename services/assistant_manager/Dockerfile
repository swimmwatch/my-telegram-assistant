FROM python:3.9

WORKDIR /app

COPY . .

RUN apt update -y

# Install poetry
RUN apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "-m", "services.assistant_manager.main"]