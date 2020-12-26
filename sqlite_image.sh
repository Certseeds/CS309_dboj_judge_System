#!/bin/sh
name="${1}"
name=sqlite_test
outside_Port="${2}"
  #-p ${outside_Port}:3306 \
  #-e MYSQL_ROOT_PASSWORD=123456 \
docker run -itd \
  --name "${name}" \
  -v "${HOME}"/docker_dir/sqlite:/tmp/folder \
  nouchka/sqlite3

echo "!23"