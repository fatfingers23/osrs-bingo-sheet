# Build the webpage
FROM node:lts-alpine3.18 as frontend
WORKDIR /frontend-app
COPY ./frontend /frontend-app
RUN npm install
RUN npm run build

FROM ubuntu:22.04
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y \
    pip \
    python3.11 \
	nano \
	curl \
	ca-certificates \
	sudo \
  && rm -rf /var/lib/apt/lists/*


EXPOSE 5000

# Copy over backenc files
COPY insomniacs /app/insomniacs
COPY bingo_app.ini /etc/bingo_app.ini
COPY frontend/src/bingoSheet.json /etc/bingoSheet.json

# Copy over webpage and move everything to be hosted from /srv
COPY --from=frontend /frontend-app/dist /srv

# Install Python app and dependencies
WORKDIR /app
RUN python3.11 -m pip install -r /app/insomniacs/requirements.txt
CMD python3.11 -m insomniacs