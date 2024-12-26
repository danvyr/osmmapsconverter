wget https://raw.githubusercontent.com/tbicr/osm-name-migrate/refs/heads/main/osm_back.py -O osm_back.py
docker build .  -t osm_back:latest
