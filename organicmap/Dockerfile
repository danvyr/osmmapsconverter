# FROM ubuntu:21.10 AS builder
FROM ubuntu:22.04 AS builder

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && DEBIAN_FRONTEND="noninteractive"  apt-get install -y \
    build-essential \
    cmake \
    git \
    clang \
    python2 \
    python3-pip \
    qtbase5-dev \
    libqt5svg5-dev \
    libc++-dev \
    libboost-iostreams-dev libboost-thread*-dev\
    libgl1-mesa-dev  \
    libglu1-mesa-dev \
    libsqlite3-dev \
    magics++ \
    zlib1g-dev \
    libfreetype6-dev



WORKDIR /organicmaps

COPY organicmaps /organicmaps

RUN echo "" | /organicmaps/configure.sh

RUN /organicmaps/tools/unix/build_omim.sh -rs generator_tool world_roads_builder_tool



FROM ubuntu:22.04 AS generator_tool

LABEL version="1.0"
LABEL org.opencontainers.image.authors=="danvyr@gmail.com"


ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH $PYTHONPATH:/organicmaps/organicmaps/tools/python

ARG HOME_DIR=/organicmaps
ARG USER=organicmaps

WORKDIR $HOME_DIR

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && DEBIAN_FRONTEND="noninteractive"  apt-get install -y \
    python2 \
    python3-pip \
    qtbase5-dev \
    gettext-base \
    software-properties-common \
    python3-distutils \
    python3-apt

RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install python3.8 -y
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

    
RUN mkdir -p $HOME_DIR/organicmaps/data/borders \
    $HOME_DIR/organicmaps/tools/python/maps_generator/var/etc/ \
    $HOME_DIR/maps_build \
    $HOME_DIR/out 

RUN useradd -d $HOME_DIR -s /bin/bash $USER \
        && chown $USER:$USER $HOME_DIR -R

USER $USER

COPY --chown=$USER --from=builder /organicmaps/tools/osmctools    $HOME_DIR/organicmaps/tools/osmctools
COPY --chown=$USER --from=builder /organicmaps/tools/python       $HOME_DIR/organicmaps/tools/python
COPY --chown=$USER --from=builder /organicmaps/data               $HOME_DIR/organicmaps/data
COPY --chown=$USER --from=builder /omim-build-release             $HOME_DIR/omim-build-release


RUN pip3 install -r $HOME_DIR/organicmaps/tools/python/maps_generator/requirements_dev.txt

COPY --chown=$USER   map_generator.ini.template     $HOME_DIR/
COPY --chown=$USER   generate_map.sh                $HOME_DIR/
COPY --chown=$USER   move_result.py                 $HOME_DIR/

ENTRYPOINT ["bash", "generate_map.sh"]

