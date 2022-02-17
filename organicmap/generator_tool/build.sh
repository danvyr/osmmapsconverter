#!/bin/bash
git submodule update --init --recursive
git pull


HOME_DIR=organicmaps
SOURCE=/home/ubuntu/organicmaps
BUILD_DIR=/home/ubuntu

rm -rf $HOME_DIR

mkdir -p $HOME_DIR/organicmaps/data/borders \
    $HOME_DIR/organicmaps/tools/python/maps_generator/var/etc/ \
    $HOME_DIR/maps_build 

cp -r $SOURCE/tools/osmctools    $HOME_DIR/organicmaps/tools/
cp -r $SOURCE/tools/python       $HOME_DIR/organicmaps/tools/
cp -r $SOURCE/data               $HOME_DIR/organicmaps/
cp -r $BUILD_DIR/omim-build-release    $HOME_DIR
cp map_generator.ini.template     $HOME_DIR/organicmaps/tools/python/maps_generator/var/etc/
cp generate_map.sh                $HOME_DIR/
rm -rf $HOME_DIR/organicmaps/tools/python/maps_generator/var/etc/map_generator.ini


cp Dockerfile generate_map.sh map_generator.ini.template $HOME_DIR\
cd $HOME_DIR

docker build -t organicmap_mapgenerator:master  .
