FROM python:3.8-slim as base

RUN adduser --disabled-password pynecone

FROM base as build

WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install wheel \
    && pip install -r requirements.txt

FROM base as runtime

RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/app/venv/bin:$PATH"

FROM runtime as init

WORKDIR /app
ENV BUN_INSTALL="/app/.bun"
COPY --from=build /app/ /app/

RUN pc init 

RUN bash -c "/app/.bun/bin/bun install --cwd .web/"

RUN echo "export BUN_INSTALL=$BUN_INSTALL" >> ~/.bashrc

RUN echo "The bun installation is located in: $(which bun)"

FROM runtime

COPY --chown=pynecone --from=init /app/ /app/
USER pynecone
WORKDIR /app

CMD ["pc","run" , "--env", "prod"]

EXPOSE 3000
EXPOSE 8000
