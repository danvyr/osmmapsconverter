FROM openjdk:25-jdk-slim


LABEL version="1.0"
LABEL org.opencontainers.image.authors=="danvyr@gmail.com"

ARG HOME_DIR=/OsmAndMapCreator
ARG USER=osmand
ARG GROUP=1000



RUN mkdir $HOME_DIR && useradd -d $HOME_DIR -s /bin/bash -u 1000 $USER && mkdir -p /out /in && chown $USER:$GROUP $HOME_DIR -R

USER $USER
WORKDIR /OsmAndMapCreator

COPY --chown=$USER generate_map.sh .
COPY --chown=$USER OsmAndMapCreator/ /OsmAndMapCreator


ENTRYPOINT ["bash", "generate_map.sh"]
