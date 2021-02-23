# Create a docker image for the DNS application

# Setup the base image
FROM phusion/passenger-full

# Set correct environment variables.
ENV HOME /root
ENV DATABASE_URL='sqlite:////var/lib/powerdns/pdns.sqlite3'
ENV FLASK_APP='/flaskapp/dns_api.py'

# Use baseimage-docker's init process.
###############################################################################
# DNS Setup stage
##############################################################################
#setup pdns repo
RUN apt-get update && apt-get install -y curl sudo \
	&& curl https://repo.powerdns.com/FD380FBB-pub.asc | sudo apt-key add - \
	&& echo "deb [arch=amd64] http://repo.powerdns.com/ubuntu groovy-auth-${VERSION} main" > /etc/apt/sources.list.d/pdns.list

# Install the powerdns service
RUN /bin/bash -c 'apt-get install pdns-server -y'
RUN /bin/bash -c 'apt-get install pdns-backend-sqlite3 -y'

# copy the config files and db files to docker image
COPY assets/powerdns_config/* /etc/powerdns/
COPY assets/pdns_db/ /var/lib/powerdns/

#expose the dns service port
EXPOSE 53/udp

##################################################################################
# API Service setup stage
#################################################################################
# Copy over files to the application directory
COPY app/* /flaskapp/app/
COPY requirements.txt /flaskapp/
COPY config.py /flaskapp/
COPY dns_api.py /flaskapp/

# Install the requirements into the python environment
RUN apt-get install python3-pip -y
RUN pip3 install -r /flaskapp/requirements.txt

EXPOSE 5000/tcp


##################################################################################
# Node frontend mappings
#################################################################################
# Copy the frontend application files into the container
COPY frontend/dnsmodifier/ /node-frontend/
WORKDIR node-frontend
RUN rm package-lock.json
RUN npm install
RUN npm run build
RUN npm install -g serve
EXPOSE 3000/tcp


# Start container

# ENTRYPOINT service pdns start && flask run > flasklogs.log & && bash
ENTRYPOINT service pdns start && (flask run --host=0.0.0.0 &) && (cd /node-frontend && serve -l 3000 -s build &) && cd / && bash
