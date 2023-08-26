FROM ubuntu:20.04

LABEL maintainer "arubattino@conae.gov.ar"

# Install some packages
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y \ 
      python3.9 \ 
      python3.9-dev \ 
      net-tools \
      ffmpeg \
      libsm6 \
      libxext6 \
      vim \
      xorg \
      unzip \
      wget \
      curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download the MCR from MathWorks site an install with -mode silent
RUN mkdir /mcr-install && \
    mkdir /opt/mcr && \
    cd /mcr-install && \
    wget --no-check-certificate -q https://ssd.mathworks.com/supportfiles/downloads/R2018b/deployment_files/R2018b/installers/glnxa64/MCR_R2018b_glnxa64_installer.zip && \
    unzip -q MCR_R2018b_glnxa64_installer.zip && \
    rm -f MCR_R2018b_glnxa64_installer.zip && \
    ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent && \
    cd / && \
    rm -rf mcr-install

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH /opt/mcr/v95/runtime/glnxa64:/opt/mcr/v95/bin/glnxa64:/opt/mcr/v95/sys/os/glnxa64:/opt/mcr/v95/extern/bin/glnxa64
ENV XAPPLRESDIR /etc/X11/app-defaults

# SNAP
RUN mkdir /snap-install && \
    mkdir /opt/snap && \
    cd /snap-install && \
    wget --no-check-certificate -q https://download.esa.int/step/snap/9.0/installers/esa-snap_all_unix_9_0_0.sh && \
    chmod 777 -R esa-snap_all_unix_9_0_0.sh && \
    ./esa-snap_all_unix_9_0_0.sh -q && \
    cd / && \
    rm -rf snap-install


WORKDIR /src
