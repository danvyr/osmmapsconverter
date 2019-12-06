FROM 761dc26035a6:mapsme

WORKDIR /mapsme

RUN apt-get install python3-pip -y
#RUN ls /
RUN cd /mapsme/tools/python/maps_generator

RUN ls

RUN cd /mapsme/tools/python/maps_generator && pip3 install -r requirements.txt

RUN cp map_generator.ini /mapsme/tools/python/maps_generator/var/etc/map_generator.ini

CMD cd /mapsme/tools/python/maps_generator &&  python3.6 -m maps_generator --countries="Belarus"



#https://github.com/mapsme/omim/tree/master/tools/python/maps_generator

#tools/unix/build_omim.sh -r



