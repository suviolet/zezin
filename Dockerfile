FROM python:3.7.3-slim

ENV PYTHONUNBUFFERED 1

ARG UID
ARG GID
ARG COMMAND
ENV RUN_COMMAND=${COMMAND}

RUN echo "Container UID: $UID"
RUN echo "Container GID: $GID"
RUN echo "run_command= $RUN_COMMAND"

RUN apt-get update \
&& apt-get install -y --no-install-recommends \
tree build-essential libssl-dev libffi-dev

RUN mkdir /tmp/requirements
COPY requirements/* /tmp/requirements/

RUN tree /tmp/requirements \
&& pip install --upgrade pip \
&& pip install -r /tmp/requirements/base.txt

RUN groupadd -r -g "$GID" appuser; useradd -l --create-home -u "$UID" -g "$GID" appuser
WORKDIR /home/appuser
COPY . /home/appuser

RUN /bin/bash -l -c 'chown -R "$UID:$GID" /home/appuser'

USER appuser
RUN echo "User details: $(id)" && ls -la /home/appuser

EXPOSE 5000

ENTRYPOINT make ${RUN_COMMAND}