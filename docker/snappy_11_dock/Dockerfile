FROM ubuntu:22.04

LABEL maintainer "gus838@gmail.com"

# Install some packages
RUN apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential \
      python3.10 \
      python3.10-dev \
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


# Install other packages
RUN apt update
RUN apt install wget -y
RUN apt install dos2unix -y
RUN apt install git -y


# Definición de carpeta de trabajo
ARG SOURCE_PATH=/src
WORKDIR $SOURCE_PATH

#############################################################
############### Instalación completa SNAP 11.0 ##############
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
# RUN apt install python3.6-distutils -y
RUN apt install python3-venv python3-pip -y
RUN pip install pybridge
RUN git clone https://github.com/bcdev/jpy
ARG JPY=$PYBRIDGE_FOL/jpy
# # #TODO fix on forman committed on May 18 1 parent ff48ea0 commit 76548cb6f3b9ba795ed6b3a42327607234eaba3c

##maven
ARG MAVEN_INST=${SOURCE_PATH}/maven_install
WORKDIR $MAVEN_INST
RUN wget https://archive.apache.org/dist/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz
RUN tar xzvf apache-maven-3.8.6-bin.tar.gz
ENV PATH $PATH:$MAVEN_INST/apache-maven-3.8.6/bin
# Línea agregada por Rama para probar si pasa la línea de instalación de jpy
# RUN pip install wheel
# RUN cd $JPY && python3 setup.py build maven bdist_wheel


# # SNAP
ARG SNAP=${SOURCE_PATH}/snap2compile
ARG SNAP_INST=/opt/snap
RUN mkdir $SNAP
ENV DISPLAY=""
RUN mkdir ${SNAP_INST} && \
    cd ${SNAP} && \
    wget --no-check-certificate -q https://download.esa.int/step/snap/11.0/installers/esa-snap_all_linux-11.0.0.sh && \
    chmod 777 -R esa-snap_all_linux-11.0.0.sh && \
    ./esa-snap_all_linux-11.0.0.sh -q

