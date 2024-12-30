#!/bin/bash

echo ""
echo "[INFO] Moving tag name:ru to name"
echo "[INFO] ENV:"
echo PBF_FILE="$PBF_FILE"
echo PBF_FILE_RU="$PBF_FILE_RU"
echo ""

if [[ -n  "$PBF_FILE" && -n "$PBF_FILE_RU"  ]]
then
    python3 osm_back.py -l ru -o  "/pbf/$PBF_FILE_RU" "/pbf/$PBF_FILE"
    
    status=$?
    if   [ $status -eq 0 ]
    then
        echo "[INFO] Moving tag name:ru to name Successful"
    else
        echo "[INFO] Moving tag name:ru to name Successful Failed"   
    fi
else
    echo "[INFO] Not all files are set"
fi


