FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv python3-networkx python3-numpy \
        curl ca-certificates jq git \
    && rm -rf /var/lib/apt/lists/*
COPY probe /usr/local/bin/probe
RUN chmod 755 /usr/local/bin/probe
WORKDIR /app
