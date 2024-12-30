FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
        apt-get install -y osmium-tool python3-pyosmium python3-shapely --no-install-recommends && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* && \
        mkdir -p /pbf

COPY osm_back.* .

ENTRYPOINT [ "bash" , "osm_back.sh"]
