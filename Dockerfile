FROM ubuntu:20.04 AS base

ENV USER=pyrunner
ENV UID=12345
ENV GID=23456

ENV HOME /home/pyrunner
ENV PATH $HOME:$PATH
# because pip packages are installed to $HOME/.local/
ENV PATH $HOME/.local/bin:$PATH

ENV APT_PYTHON_VERSION=python3.9

RUN addgroup --gid "$GID" "$USER" && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "$HOME" \
    --ingroup "$USER" \
    --uid "$UID" \
    "$USER"

RUN apt update \
  && apt install -y software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa && apt install -y $APT_PYTHON_VERSION \
  && ln -sf /usr/bin/$APT_PYTHON_VERSION /usr/bin/python3 \
  && apt install -y python3-pip

USER pyrunner

CMD ["python3"]


FROM base

ADD app/* $HOME/
ADD portfolio.json $HOME/

RUN pip3 install --upgrade pip
RUN pip3 install -r $HOME/requirements.txt

CMD sleep 15 && python3 $HOME/main.py
