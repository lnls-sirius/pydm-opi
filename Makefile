.PHONY: install

install:
	apt-get -y install python3-pip python3-dev &&\
	pip3 install virtualenv==16.0.0 && \
	virtualenv .virtualenv && \
        cd install && ./setup-env.sh

