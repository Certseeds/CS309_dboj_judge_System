FROM mysql

RUN apt update && \
  apt upgrade && \
  apt install ps &&\
  echo "bind-address=0.0.0.0" >> /etc/my.cnf &&\
  echo "bind-address=0.0.0.0" >> /etc/mysql/my.cnf &&\
  echo "bind-address=0.0.0.0" >> /etc/mysql/mysql.conf.d/mysqld.cnf
