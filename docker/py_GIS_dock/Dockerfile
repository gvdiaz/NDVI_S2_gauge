FROM ubuntu:22.04

LABEL maintainer "gus838@gmail.com"

# Install some packages
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y \ 
      python3.10 \ 
      libpython3.10-dev \
      python3-pip \
      net-tools \
      ffmpeg \
      libsm6 \
      libxext6 \
      vim \
      xorg \
      unzip \
      wget \
      curl \
      software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# # SNAP
# RUN mkdir /snap-install && \
#     mkdir /opt/snap && \
#     cd /snap-install && \
#     wget --no-check-certificate -q https://download.esa.int/step/snap/9.0/installers/esa-snap_all_unix_9_0_0.sh && \
#     chmod 777 -R esa-snap_all_unix_9_0_0.sh && \
#     ./esa-snap_all_unix_9_0_0.sh -q

# RUN cd /opt/snap/bin && \
#     ./snappy-conf /usr/bin/python3 /usr/local/lib/python3.10/dist-packages && \
#     cd / && \
#     rm -rf snap-install

# Install GDAL
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update && \
      apt-get install -y \
      gdal-bin \
      libgdal-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip3 install GDAL

ARG source_req=./aux_files/requirements_casa.txt
ARG dest_req=/tmp_gdal/requirements.txt
RUN mkdir /tmp_gdal

COPY ${source_req} ${dest_req}
RUN cat ${dest_req}
RUN pip3 install -r ${dest_req}
RUN pip3 install openpyxl

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

EXPOSE 8888
WORKDIR /src
# CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
