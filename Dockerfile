ARG USERNAME=beddy
ARG USER_UID=501
ARG USER_GID=$USER_UID

FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get install -y dumb-init && apt-get clean

ARG USERNAME USER_UID USER_GID
RUN groupadd -g ${USER_GID} ${USERNAME} && useradd -m -u ${USER_UID} -g ${USERNAME} -s /bin/bash ${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}
ENV USER=${USERNAME} SHELL=/bin/bash

RUN python3 -m venv /home/${USERNAME}/venv
ENV PATH=/home/${USERNAME}/venv/bin:${PATH}

RUN python3 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

COPY beddy.py /home/${USERNAME}/beddy/beddy.py
WORKDIR /home/${USERNAME}/beddy

ENTRYPOINT [ "dumb-init", "hypercorn", "-b", "127.0.0.1", "beddy:app" ]
