#!/bin/bash

GIT_TAG=""
IMAGE_NAME="danvyr/organicmap"
IMAGE_DATE=`date '+%Y%m%d'`

echo "[INFO] IMAGE_DATE = $IMAGE_DATE"
if [ -d "organicmaps" ] 
then
    echo "[INFO] organicmaps exists"    
    cd organicmaps
    echo "[INFO] update organicmaps" 
    git pull
    echo "[INFO] update submodule" 
    git submodule update --init --recursive
    echo "[INFO] update complete" 
    GIT_TAG=`git rev-parse --short HEAD`
    cd ..
else
    echo "[INFO] organicmaps does not exists."
    git clone -b master --single-branch --recurse-submodules -j8  https://github.com/organicmaps/organicmaps.git 
    echo "[INFO] update complete" 
    cd organicmaps
    GIT_TAG=`git rev-parse --short HEAD`
    cd ..
fi


echo "[INFO] GIT_TAG =  $GIT_TAG"  

docker build -t $IMAGE_NAME:latest -t $IMAGE_NAME:$IMAGE_DATE -t $IMAGE_NAME:$GIT_TAG  .

echo "docker push $IMAGE_NAME:latest"
docker push $IMAGE_NAME:latest

echo "docker push $IMAGE_NAME:$IMAGE_DATE"
docker push $IMAGE_NAME:$IMAGE_DATE

echo "docker push $IMAGE_NAME:$GIT_TAG"
docker push $IMAGE_NAME:$GIT_TAG