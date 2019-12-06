#!/bin/bash

CURRENT_DIR=$(pwd)

#create mapsme generator

cd $CURRENT_DIR/mapsme
echo `pwd`
#git clone --depth=1 --recursive https://github.com/mapsme/omim.git

#need 4GB RAM to build
#sudo docker build . -t mapsme-gen


#download and setup osmand generator
mkdir $CURRENT_DIR/osmand/OsmAndMapCreator/

cd $CURRENT_DIR/osmand
echo `pwd`

wget http://download.osmand.net/latest-night-build/OsmAndMapCreator-main.zip

unzip OsmAndMapCreator-main.zip -d $CURRENT_DIR/osmand/OsmAndMapCreator/

#sudo docker build . -t osmand-crtr
