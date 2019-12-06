FROM ubuntu:18.04

WORKDIR /mapsme

COPY omim /mapsme 

RUN apt-get update && RUN apt-get upgrade -y

RUN apt-get install qtbase5-dev cmake libsqlite3-dev clang libc++-dev libboost-iostreams-dev libglu1-mesa-dev python3-pip -y

RUN cd omim && echo | ./configure.sh

RUN ./tools/unix/build_omim.sh -sr generator_tool

RUN cd /mapsme/omim/tools/python/maps_generator && pip3 install -r requirements.txt

#RUN cp map_generator.ini /mapsme/tools/python/maps_generator/var/etc/map_generator.ini

#CMD cd /mapsme/tools/python/maps_generator &&  python3.6 -m maps_generator --countries="Belarus"



#https://github.com/mapsme/omim/tree/master/tools/python/maps_generator

#tools/unix/build_omim.sh -r


