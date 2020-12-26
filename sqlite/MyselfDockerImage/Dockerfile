FROM debian:stable-slim
MAINTAINER Certseeds "51754303+Certseeds@users.noreply.github.com"
RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get -yq --no-install-recommends install sqlite3=3.* && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
	mkdir -p /root/db
WORKDIR /root/db
ENTRYPOINT [ "sqlite3","daemon off;"]