###########
# BUILDER #
###########

# multistage build
FROM python:3.12.1-slim-bookworm as builder

RUN apt-get update \
&& apt-get -y install ca-certificates git openssh-client

RUN mkdir -p -m 0700 /root/.ssh && ssh-keyscan "github.com" >> /root/.ssh/known_hosts

WORKDIR /usr/src/app

RUN --mount=type=ssh \
ssh -T git@github.com || true \
&& git clone git@github.com:margaretlange/ollama-deep-researcher.git 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pwd
# create shells
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels /usr/src/app/ollama-deep-researcher 

#########
# FINAL #
#########

# pull official base image
FROM python:3.12.1-slim-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-traditional gcc postgresql \
  && apt-get clean

# install python dependencies
COPY --from=builder /usr/src/app/wheels /usr/src/app/wheels
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache /usr/src/app/wheels/*
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
