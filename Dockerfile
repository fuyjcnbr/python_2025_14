FROM ubuntu:24.04

RUN apt update

###############python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt -y install python3-pip
RUN python -m pip install --break-system-packages uv


RUN mkdir /src

# COPY uv.lock /uv.lock
# COPY pyproject.toml /pyproject.toml
#
# RUN uv sync

WORKDIR /src