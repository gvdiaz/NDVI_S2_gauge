FROM ubuntu:20.04

LABEL maintainer "gus838@gmail.com"

# Install some packages
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y \ 
      python3.9 \ 
      python3.9-dev \
      python3-pip \
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


# SNAP
RUN mkdir /snap-install && \
    mkdir /opt/snap && \
    cd /snap-install && \
    wget --no-check-certificate -q https://download.esa.int/step/snap/9.0/installers/esa-snap_all_unix_9_0_0.sh && \
    chmod 777 -R esa-snap_all_unix_9_0_0.sh && \
    ./esa-snap_all_unix_9_0_0.sh -q && \
    cd / && \
    rm -rf snap-install

# Install GDAL
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update && \
      apt-get install gdal-bin \
      apt-get install libgdal-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install GDAL

ARG source_req=./aux_files/requirements_casa.txt
ARG dest_req=/tmp_gdal/requirements.txt
RUN mkdir /tmp_gdal

COPY ${source_req} ${dest_req}
RUN pip3 install -r ${dest_req}

WORKDIR /src
