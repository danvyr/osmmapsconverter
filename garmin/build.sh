#!/bin/sh



#build map


#java -jar split/splitter.jar --output-dir=temp ../in/belarus.osm.pbf

cd temp
java -jar ../mkgmap/mkgmap.jar --route --add-pois-to-areas --bounds=bounds --index  --gmapsupp --mapname=80808080  --link-pois-to-ways  --country-name=Belarus --country-abbr=BY  6324*.osm.pbf



