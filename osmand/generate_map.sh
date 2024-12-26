#!/bin/bash

echo ""
echo "[INFO] OSMand Map Creator"
echo "[INFO] ENV:"
echo JAVA_OPT="$JAVA_OPT"
echo PBF_FILE="$PBF_FILE"
echo ""

if [[ -n  "$PBF_FILE" || -n "$JAVA_OPT" ]]
then
    java -Djava.util.logging.config.file=/OsmAndMapCreator/logging.properties  $javaOpt  -cp /OsmAndMapCreator/OsmAndMapCreator.jar:/OsmAndMapCreator/lib/*.jar net.osmand.MainUtilities generate-obf   /in/$PBF_FILE
    
    status=$?
    if   [ $status -eq 0 ]
    then
        ls -l /OsmAndMapCreator/*.obf
        echo "[INFO] Move Result to out"
        mv -v /OsmAndMapCreator/*.obf /out/
    else
        echo "[INFO] converting failed"   
    fi
else
    echo "[INFO] Not all parameters are set"
fi


