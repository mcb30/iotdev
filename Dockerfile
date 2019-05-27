# Automated tester container
#

FROM fedora

WORKDIR /opt/iotdev

USER root

RUN dnf update -y

RUN dnf install -y python3-coverage python3-orderedset

COPY . .

CMD ./test.sh
