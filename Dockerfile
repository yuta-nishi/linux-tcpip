FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    bash \
    bind9-dnsutils \
    coreutils \
    curl \
    dnsmasq-base \
    grep \
    iproute2 \
    iptables \
    iputils-ping \
    isc-dhcp-client \
    netcat-openbsd \
    procps \
    python3 \
    sudo \
    tcpdump \
    traceroute \
    vim \
    wget

WORKDIR /workdir
