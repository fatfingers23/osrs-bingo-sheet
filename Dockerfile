FROM ubuntu:22.04
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y \
    pip \
    python3 \
	nano \
	curl \
	ca-certificates \
	sudo \
  && rm -rf /var/lib/apt/lists/*

# Needs to happen get new enough nodejs version
RUN curl -sL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
RUN chmod +x nodesource_setup.sh
RUN sudo ./nodesource_setup.sh
RUN apt-get install nodejs -y

EXPOSE 5000

COPY frontend /app/frontend
COPY insomniacs /app/insomniacs
COPY bingo_app.ini /etc/bingo_app.ini

# Build webpage and move everything to be hosted from /srv
WORKDIR /app/frontend
RUN npm install
RUN npm run build
RUN cp -r dist/* /srv

# Install Python app and dependencies
WORKDIR /app
RUN pip install -r /app/insomniacs/requirements.txt
CMD python3 -m insomniacs