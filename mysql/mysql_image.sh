#!/bin/sh
name="${1}"
outside_Port="${2}"
docker run -itd \
  --name "${name}" \
  -p ${outside_Port}:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -v "${HOME}"/docker_dir/mysql:/tmp/folder \
  mysql

echo "!23"