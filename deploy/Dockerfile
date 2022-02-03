ARG VERSION

FROM python:3.8.5-slim-buster AS base
LABEL description="TicTacToe"

RUN apt-get update \
    && apt-get install -y  \
        locales \
        locales-all \
#        libpq-dev \
    && locale-gen en_US.UTF-8 \
    && apt-get update

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN useradd -ms /bin/bash user \
    && mkdir -p /home/project/dist/ \
    && chown -R user:user /var /home /etc/fstab

COPY / /home/project/dist/


RUN python -m pip install -r /home/project/dist/requirements.txt --no-cache-dir

USER user
WORKDIR /home/project/dist
ENV DJANGO_SETTINGS_MODULE=tic_tac_toe.settings

FROM base AS prod

USER root
RUN apt-get clean \
    && apt-get autoclean \
    && apt-get remove -y \
        gcc \
        unzip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


