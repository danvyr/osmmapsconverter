wget https://raw.githubusercontent.com/tbicr/osm-name-migrate/refs/heads/main/osm_back.py -O osm_back.py

IMAGE_NAME="danvyr/osm_back"
IMAGE_DATE=`date '+%Y%m%d'`

docker build -t $IMAGE_NAME:latest -t $IMAGE_NAME:$IMAGE_DATE   .

status=$?
echo "[INFO] status = $status"
if [ $status -eq 0 ]
then
    echo ""
    echo "[INFO] docker push $IMAGE_NAME:latest"
    docker push $IMAGE_NAME:latest

    echo "[INFO] docker push $IMAGE_NAME:$IMAGE_DATE"
    docker push $IMAGE_NAME:$IMAGE_DATE

else
    echo ""
    echo "[ERROR] Docker failed"
    echo ""
fi