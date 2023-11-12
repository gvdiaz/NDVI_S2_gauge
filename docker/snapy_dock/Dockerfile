FROM ubuntu:20.04

LABEL maintainer "gus838@gmail.com"

# Install some packages
##Python3.6
RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN add-apt-repository ppa:ubuntugis/ppa -y
RUN apt install python3.6 python3.6-dev -y
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

##Wget
RUN apt update
RUN apt install wget -y
RUN apt install dos2unix -y

##JAVA
RUN apt update
RUN apt install openjdk-8-jre -y
RUN apt install openjdk-8-jdk -y
ENV JDK_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME $JDK_HOME

##pybridge
RUN apt install python3.6-distutils -y
RUN pip install pybridge
RUN git clone https://github.com/bcdev/jpy
#TODO fix on forman committed on May 18 1 parent ff48ea0 commit 76548cb6f3b9ba795ed6b3a42327607234eaba3c

##maven
RUN wget https://archive.apache.org/dist/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz
RUN tar xzvf apache-maven-3.8.6-bin.tar.gz
ENV PATH $PATH:/tf/apache-maven-3.8.6/bin
RUN cd /tf/jpy/ && python setup.py build maven bdist_wheel

##snap
RUN wget https://download.esa.int/step/snap/8.0/installers/esa-snap_all_unix_8_0.sh
RUN chmod +x esa-snap_all_unix_8_0.sh
RUN sh ./esa-snap_all_unix_8_0.sh -q -splash

##snapy
RUN /usr/local/snap/bin/snappy-conf /usr/bin/python3 /tf

##numpy
RUN pip install numpy

##gdal
#RUN NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#RUN apt install gdal-bin -y
#RUN apt install libgdal-dev -y
#ENV CPLUS_INCLUDE_PATH $CPLUS_INCLUDE_PATH:/usr/include/gdal
#ENV C_INCLUDE_PATH $C_INCLUDE_PATH:/usr/include/gdal
#ENV PATH $PATH:/usr/include/gdal
#RUN pip install GDAL
RUN wget https://download.osgeo.org/gdal/2.2.4/gdal-2.2.4.tar.gz
RUN tar xzf gdal-2.2.4.tar.gz
RUN cd gdal-2.2.4 && ./configure --with-python && make -j8 && make install
RUN pip install setuptools==57.0.0
RUN pip install gdal==2.2.4
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib/


#TODO Fix versions
RUN pip install jupyter==1.0.0
RUN pip install matplotlib==3.3.4
RUN pip install pandas==1.1.5
RUN pip install openpyxl==3.0.9
RUN pip install torch==1.10.2
RUN pip install pytorch_lightning==1.5.10
RUN pip install segmentation_models_pytorch==0.2.1
RUN pip install opencv-python-headless==4.5.5.64
RUN pip install opencv-python==4.5.5.64
RUN pip install albumentations==1.1.0
RUN pip install tqdm
RUN pip install h5py
RUN pip install opencv-python
RUN pip install earthengine_api
RUN pip install geotiff
RUN pip install rasterio
RUN pip install sklearn
RUN pip install fiona
RUN pip install geopandas
RUN pip install geojson
RUN pip install tables
RUN pip install xmltodict
RUN pip install tensorflow
RUN pip install seaborn
RUN pip install numpy -U



#utils scripts
COPY utils /tf/utils
COPY notebooks /tf/notebooks
RUN chmod +x /tf/utils/*
RUN dos2unix /tf/utils/*
RUN chmod +x /tf/notebooks/*
RUN dos2unix /tf/notebooks/*


ENV DOCKER True