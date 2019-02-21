FROM  alpine:3.8
LABEL maintainer="Panos Karkazis <pkarkazis@synelixis.com>"

RUN apk add --no-cache python3 \
    python3-dev  \
    gcc \
    libc-dev \
    py3-setuptools && \
    python3 -m ensurepip  && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN mkdir -p /opt/Monitoring
COPY ./cnf_mon/ /opt/Monitoring
RUN pip3 install -r /opt/Monitoring/requirements.txt

ADD ./cnf_mon/run.sh /opt/Monitoring/run.sh
RUN chmod 0755 /opt/Monitoring/run.sh
RUN ls -la /opt/Monitoring/*

RUN chmod -R g+w /opt/Monitoring/  

WORKDIR    /opt/Monitoring

CMD ["sh", "/opt/Monitoring/run.sh"]
