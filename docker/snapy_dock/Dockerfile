FROM ubuntu:20.04

LABEL maintainer "gus838@gmail.com"

# Install some packages
# RUN apt-get update && \
#       DEBIAN_FRONTEND=noninteractive apt-get install -y \ 
#       python3.6 \ 
#       libpython3-dev \
#       python3-pip \
#       net-tools \
#       ffmpeg \
#       libsm6 \
#       libxext6 \
#       vim \
#       xorg \
#       unzip \
#       wget \
#       curl \
#       software-properties-common && \
#       apt-get clean && \
#       rm -rf /var/lib/apt/lists/*

## Herramientas de base

##Python3.6
RUN apt update
RUN apt install software-properties-common -y
RUN apt install git -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN add-apt-repository ppa:ubuntugis/ppa -y
RUN apt install python3.6 python3.6-dev -y
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
RUN apt install -y curl

##Wget
RUN apt update
RUN apt install wget -y
RUN apt install dos2unix -y

ARG SOURCE_PATH=/src
WORKDIR $SOURCE_PATH


#############################################################
############### Instalación completa SNAP 9.0 ###############
#############################################################

# ARG JAVA_INSTALL=${WORKDIR}


##JAVA
RUN apt update
RUN apt install openjdk-8-jre -y
RUN apt install openjdk-8-jdk -y
ENV JDK_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME $JDK_HOME

##pybridge
ARG PYBRIDGE_FOL=${SOURCE_PATH}/pybridge
WORKDIR $PYBRIDGE_FOL
RUN apt install python3.6-distutils -y
RUN apt install python3-venv python3-pip -y
RUN pip install pybridge
RUN git clone https://github.com/bcdev/jpy
ARG JPY=$PYBRIDGE_FOL/jpy
#TODO fix on forman committed on May 18 1 parent ff48ea0 commit 76548cb6f3b9ba795ed6b3a42327607234eaba3c

##maven
ARG MAVEN_INST=${SOURCE_PATH}/maven_install
WORKDIR $MAVEN_INST
RUN wget https://archive.apache.org/dist/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz
RUN tar xzvf apache-maven-3.8.6-bin.tar.gz
ENV PATH $PATH:$MAVEN_INST/apache-maven-3.8.6/bin
RUN cd $JPY && python3 setup.py build maven bdist_wheel


# SNAP
ARG SNAP=${SOURCE_PATH}/snap2compile
ARG SNAP_INST=/opt/snap
RUN mkdir $SNAP
ENV DISPLAY=""
RUN mkdir ${SNAP_INST} && \
    cd ${SNAP} && \
    wget --no-check-certificate -q https://download.esa.int/step/snap/9.0/installers/esa-snap_all_unix_9_0_0.sh && \
    chmod 777 -R esa-snap_all_unix_9_0_0.sh && \
    ./esa-snap_all_unix_9_0_0.sh -q

##snapy
# RUN /usr/local/snap/bin/snappy-conf /usr/bin/python3 $SOURCE_PATH
# RUN /opt/snap/bin/snappy-conf /usr/bin/python3 ${SOURCE_PATH}
RUN apt-get install psmisc

ARG SNAPPY_CONF=$SNAP_INST/bin
WORKDIR ${SNAPPY_CONF}
# RUN ./snappy-conf /usr/bin/python3 /usr/local/lib/python3.6/dist-packages && rm -rf SNAP
# RUN ["/bin/sh", "-c", "/opt/snap/bin/snappy-conf", "/usr/bin/python3", "/usr/local/lib/python3.6/dist-packages", "&", "&&", "sleep", "30"]
RUN nohup bash -c ' /opt/snap/bin/snappy-conf /usr/bin/python3 /usr/local/lib/python3.6/dist-packages &' && \
    ps && \
    sleep 55
# RUN ps && sleep 30
# RUN ps && sleep 10
# RUN sleep 30 && killall snappy-conf

# # Install GDAL
# RUN add-apt-repository ppa:ubuntugis/ppa
# RUN apt-get update && \
#       apt-get install -y \
#       gdal-bin \
#       libgdal-dev && \
#       apt-get clean && \
#       rm -rf /var/lib/apt/lists/*
# ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
# ENV C_INCLUDE_PATH=/usr/include/gdal
# RUN pip3 install GDAL

ARG source_req=./aux_files/requirements_casa.txt
ARG dest_req=/tmp_gdal/requirements.txt
RUN mkdir /tmp_gdal

COPY ${source_req} ${dest_req}
RUN cat ${dest_req}
RUN pip3 install -r ${dest_req}

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# # EXPOSE 8888
WORKDIR $SOURCE_PATH
# CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]