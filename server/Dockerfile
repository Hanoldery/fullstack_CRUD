FROM amd64/debian:stretch

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

WORKDIR /server


# Install any needed packages specified in requirements.txt

ENV HOST 0.0.0.0

# Make port 80 available to the world outside this container
EXPOSE 4000

# Define environment variable
ENV NAME Server

ENV APP_DIRECTORY /server/

ENV DATABASE_NAME zimmer
ENV DATABASE_HOST=212.47.228.170
ENV FRONT_URL http://0.0.0.0:3000
ENV API_URL http://0.0.0.0:4000
ENV PYTHONPATH $APP_DIRECTORY:$PYTHONPATH
ENV PROJECT_PATH $APP_DIRECTORY/index

ENV DATABASE_LOGIN pierre
ENV DATABASE_PASSWORD J0R2l3w3b?!?
ENV FLASK_DEBUG true
ENV SENDGRID_API_KEY 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

ENV SECURITY_PASSWORD_SALT pierreandalexislovezimmer
ENV SECRET_KEY zimmer_website_token
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y --no-install-recommends dialog apt-utils
RUN apt-get -y install locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD requirements.txt /server/
RUN pip3 install -r requirements.txt

ADD . /server


CMD python3 server.py
