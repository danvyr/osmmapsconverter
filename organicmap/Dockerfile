FROM ubuntu:24.04 AS builder

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && DEBIAN_FRONTEND="noninteractive"  apt-get install -y \
    build-essential \
    clang \
    cmake \
    ninja-build \
    python3 \
    qt6-base-dev \
    qt6-positioning-dev \
    libc++-dev \
    libfreetype-dev \
    libglvnd-dev \
    libgl1-mesa-dev \
    libharfbuzz-dev \
    libicu-dev \
    libqt6svg6-dev \
    libqt6positioning6-plugins \
    libqt6positioning6 \
    libsqlite3-dev \
    zlib1g-dev \
    && apt-get clean


WORKDIR /organicmaps

COPY organicmaps /organicmaps

RUN echo "" | /organicmaps/configure.sh

RUN /organicmaps/tools/unix/build_omim.sh -rs generator_tool world_roads_builder_tool



FROM ubuntu:24.04 AS generator_tool

LABEL version="1.0"
LABEL org.opencontainers.image.authors=="danvyr@gmail.com"


ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH $PYTHONPATH:/organicmaps/organicmaps/tools/python
ENV TZ=Europe/London

ARG HOME_DIR=/organicmaps
ARG USER=organicmaps

RUN mkdir /organicmaps && \
    useradd -d $HOME_DIR -s /bin/bash $USER && \
    mkdir -p /organicmaps/.local/share/OMaps  && \
    chown $USER:$USER $HOME_DIR -R

WORKDIR $HOME_DIR


RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p $HOME_DIR/organicmaps/data/borders \
    $HOME_DIR/organicmaps/tools/python/maps_generator/var/etc/ \
    $HOME_DIR/maps_build \
    $HOME_DIR/out \
    $HOME_DIR/.config/OMaps


RUN apt-get update &&\
    DEBIAN_FRONTEND="noninteractive"  apt-get install  -y --no-install-recommends\
    python3 \
    qt6-base-dev \
    gettext-base \
    software-properties-common \
    python3-pip \
    python3-apt \
    osmctools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $USER

COPY --chown=$USER --from=builder /organicmaps/tools/osmctools    $HOME_DIR/organicmaps/tools/osmctools
COPY --chown=$USER --from=builder /organicmaps/tools/python       $HOME_DIR/organicmaps/tools/python
COPY --chown=$USER --from=builder /organicmaps/data               $HOME_DIR/organicmaps/data
COPY --chown=$USER --from=builder /omim-build-release             $HOME_DIR/omim-build-release

RUN python3 -m pip install -r $HOME_DIR/organicmaps/tools/python/maps_generator/requirements_dev.txt --break-system-packages

COPY --chown=$USER   map_generator.ini.template     $HOME_DIR/
COPY --chown=$USER   generate_map.sh                $HOME_DIR/
COPY --chown=$USER   move_result.py                 $HOME_DIR/

ENTRYPOINT ["bash", "generate_map.sh"]

