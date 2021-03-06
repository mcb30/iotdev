# Automated tester container
#

FROM fedora

WORKDIR /opt/iotdev

USER root

RUN dnf update -y

RUN dnf install -y python3-coverage python3-multidict python3-orderedset \
		   python3-requests

COPY . .

CMD ./test.sh
