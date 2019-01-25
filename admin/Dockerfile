# Use an official Python runtime as a parent image
FROM amd64/debian:stretch

# Set the working directory to /server
WORKDIR /web

ADD package.json /web
# Install any needed packages specified in requirements.txt


# Copy the current directory contents into the container at /server
ADD . /web

# INSTALL NODE AND NPM
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 8.9.4

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN npm install

ENV HOST 0.0.0.0

# Make port 80 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV NAME Web

RUN source ./env.sh
RUN npm rebuild node-sass
# Run server.py when the container launches
CMD npm run dev