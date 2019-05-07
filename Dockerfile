# Automated tester container
#

FROM fedora

WORKDIR /opt/iotdev

USER root

RUN dnf update -y

RUN dnf install -y python3-coverage

COPY . .

CMD ./test.sh
