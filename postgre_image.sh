#!/bin/sh
name="${1}"
name=posrgre_image
  #-p ${outside_Port}:3306 \
  #-e MYSQL_ROOT_PASSWORD=123456 \
docker run -itd \
  --name "${name}" \
  -p 5432:5432 \
  -e POSTGRES_USERNAME=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -v "${HOME}"/docker_dir/sqlite:/tmp/folder \
  frodenas/postgresql

echo "!23"