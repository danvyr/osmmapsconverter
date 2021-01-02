FROM ubuntu:18.04

WORKDIR /mapsme

COPY omim /mapsme 

RUN apt-get update && apt-get upgrade -y

RUN apt-get install qtbase5-dev cmake libsqlite3-dev clang libc++-dev libboost-iostreams-dev python-pip python3-setuptools  libglu1-mesa-dev python3-pip  libboost-tools-dev libboost-thread1.62-dev magics++ -y

RUN cd omim && git checkout release-103 && echo | ./configure.sh

RUN ./tools/unix/build_omim.sh -sr generator_tool

RUN cd tools/python/maps_generator && pip3 install -r requirements.txt

#RUN cp map_generator.ini /mapsme/omim/tools/python/maps_generator/var/etc/map_generator.ini

#CMD cd /mapsme/tools/python/ &&  python3.6 -m maps_generator --countries="Belarus*"

#cd omim/tools/python
#python$ python3.6 -m maps_generator -h


#https://github.com/mapsme/omim/tree/master/tools/python/maps_generator

#tools/unix/build_omim.sh -r

#python3.6 -m maps_generator --countries="Belarus_Minsk Region" --skip="Coastline"

#python3.6 -m maps_generator --countries="Belarus*" --skip="coastline"

#Belarus_Minsk Region	5896.8029
#Belarus_Vitebsk Region	2127.155647
#Belarus_Hrodna Region	1980.810717
#Belarus_Brest Region	1459.825411
#Belarus_Maglieu Region	1427.459736
#Belarus_Homiel Region	1426.153685
