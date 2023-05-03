FROM python:3.8

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    curl -fsSL https://bun.sh/install | bash

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY package.json ./
# RUN npm install

COPY . .

RUN pc init

EXPOSE 3000
EXPOSE 8000

ENTRYPOINT [ "pc", "run" ]
CMD ["--env", "prod"]
