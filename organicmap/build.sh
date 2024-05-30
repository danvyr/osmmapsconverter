#!/bin/bash

GIT_TAG=""
IMAGE_NAME="danvyr/organicmap"
IMAGE_DATE=`date '+%Y%m%d'`

echo "[INFO] IMAGE_DATE = $IMAGE_DATE"
if [ -f "organicmaps/README.md" ]
then
    echo "[INFO] organicmaps exists"
    pwd
    cd organicmaps
    pwd
    echo "[INFO] update organicmaps"
    git pull
    echo "[INFO] update submodule"
    git submodule update --init --recursive
    echo "[INFO] update complete"
    GIT_TAG=`git rev-parse --short HEAD`
    cd ..
    pwd
else
    echo "[INFO] organicmaps does not exists."
    git clone -b master --single-branch --recurse-submodules -j8  https://github.com/organicmaps/organicmaps.git
    echo "[INFO] update complete"
    pwd
    cd organicmaps
    pwd
    GIT_TAG=`git rev-parse --short HEAD`
    cd ..
    pwd
fi
echo ""

echo "[INFO] Copy  exceptions.py to organicmaps/tools/python/maps_generator/generator/exceptions.py"

cp exceptions.py organicmaps/tools/python/maps_generator/generator/exceptions.py

echo ""

echo "[INFO] GIT_TAG =  $GIT_TAG"

echo ""

docker build -t $IMAGE_NAME:latest -t $IMAGE_NAME:$IMAGE_DATE -t $IMAGE_NAME:$GIT_TAG  .

status=$?
echo "[INFO] status = $status"
if [ $status -eq 0 ]
then
    echo ""
    echo "[INFO] docker push $IMAGE_NAME:latest"
    docker push $IMAGE_NAME:latest

    echo "[INFO] docker push $IMAGE_NAME:$IMAGE_DATE"
    docker push $IMAGE_NAME:$IMAGE_DATE

    echo "[INFO] docker push $IMAGE_NAME:$GIT_TAG"
    docker push $IMAGE_NAME:$GIT_TAG
    echo ""
else
    echo ""
    echo "[ERROR] Docker failed"
    echo ""
fi