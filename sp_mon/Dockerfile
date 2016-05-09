FROM ubuntu:14.04

RUN apt-get -y install apt-transport-https ca-certificates && \
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D && \
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >> /etc/apt/sources.list.d/docker.list && \
apt-get update && apt-get -y upgrade && \
apt-get -y install python2.7 python2.7-dev python-pip docker-engine=1.10.2-0~trusty nano && \
pip install docker-py 
 
RUN mkdir -p /opt/Monitoring
COPY ./ /opt/Monitoring

ADD ./run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN ls -la /opt/Monitoring/*

CMD ["/opt/Monitoring/run.sh"]