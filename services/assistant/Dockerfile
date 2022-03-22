FROM python:3.9

WORKDIR /app

COPY . .

# Install dependencies for TDLib
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libssl-dev \
    libc++-dev \
    libc++abi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "python", "-m", "services.assistant.main"]