#!/bin/sh

<<<<<<< HEAD

#build map

cd temp

java -jar split/splitter.jar --output-dir=temp ../in/belarus.osm.pbf
cd temp
java -jar ../mkgmap/mkgmap.jar   --route --add-pois-to-areas --bounds=bounds --index  --gmapsupp --mapname=80808080 --country-name=Belarus --country-abbr=BY  6324*.osm.pbf
mv gmapsupp.img ../../out



=======
#prepare
wget http://www.mkgmap.org.uk/download/mkgmap-r4425.tar.gz

mkdir mkgmap
tar -xf mkgmap-r4425.tar.gz --directory mkgmap
mv mkgmap/mkgmap-r4425/* mkgmap
rmdir mkgmap/mkgmap-r4425

rmdir split
mkdir split

wget http://www.mkgmap.org.uk/download/splitter-r595.tar.gz

tar -xf splitter-r595.tar.gz  --directory  split
mv split/splitter-r595/* split
rmdir split/splitter-r595

#build map
java -jar splitter.jar --output-dir=temp ../in/belarus.osm.pbf 

java -jar mkgmap/mkgmap.jar   --route --add-pois-to-areas --bounds=bounds --index  --gmapsupp --mapname=80808080 --country-name=Belarus --country-abbr=BY   --output-dir  ../out
>>>>>>> refs/remotes/origin/master


