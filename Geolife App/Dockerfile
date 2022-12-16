FROM arm64v8/python:3.8-slim

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Most of the below is taken from https://github.com/microsoft/vscode-dev-containers/tree/master/containers/python-3-miniconda/.devcontainer
# ...we're just starting from an aarch64 base image

# [Option] Install zsh
ARG INSTALL_ZSH="true"
# [Option] Upgrade OS packages to their latest versions
ARG UPGRADE_PACKAGES="true"

# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
COPY library-scripts/common-debian.sh /tmp/library-scripts/
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    && apt-get purge -y imagemagick imagemagick-6-common \
    # Install common packages, non-root user
    && bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

RUN apt-get update
RUN apt-get install -y --fix-missing curl autoconf libtool automake python3-pip libgdal-dev locales
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip install setuptools==57.5.0
RUN pip install GDAL==3.0.4
RUN curl -L https://github.com/libspatialindex/libspatialindex/archive/1.8.5.tar.gz | tar -xz
RUN cd libspatialindex-1.8.5 && ./autogen.sh && ./configure && make && make install && ldconfig

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

USER vscode

# TODO: MD5 check
RUN cd && wget -O Miniforge3.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh && \
    bash Miniforge3.sh -b && \
    rm Miniforge3.sh

ENV PATH /home/vscode/miniforge3/bin:$PATH

RUN conda install streamlit

CMD streamlit run --server.port $PORT 🏡_Home.py