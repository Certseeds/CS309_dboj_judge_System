#!/bin/bash
set pipefail
oldhash="$(cat /proc/sys/kernel/random/uuid)"
echo ${oldhash}
hash="${oldhash:0:8}"
enter(){
  echo $(pwd)
  cd /tmp/folder
  echo $(pwd)
}
build_mysqlFiles(){
  echo "[client]
protocol=tcp
host=127.0.0.1
user=root
password=123456
port=3306
" > "${HOME}"/.mysql
  echo "[client]
port=3306" > /etc/my.cnf
  echo "CREATE DATABASE ${hash} DEFAULT CHARACTER SET utf8mb4;" > buildDataBase.sql  
}
build_database(){
  echo $(date)
  mysql --defaults-file="${HOME}"/.mysql < buildDataBase.sql
  #mysql -h 127.0.0.1 -P 3306 -uroot -p < buildDataBase.sql
}
build_tables(){
  echo $(date)
  mysql --defaults-file="${HOME}"/.mysql -D${hash} < createTable.sql
}
run_tables(){
  echo $(date)
  mysql --defaults-file="${HOME}"/.mysql -D${hash} < searchTable.sql > result.log
}
main2(){
    echo "[client]
protocol=tcp
host=127.0.0.1
user=root
password=123456
port=3310
" > "${HOME}"/.mysql
echo "CREATE DATABASE tempTable DEFAULT CHARACTER SET utf8mb4;" > buildDataBase.sql  
  mysql --defaults-file="${HOME}"/.mysql < buildDataBase.sql
}
main(){
  #echo "begin"
  #cat /etc/mysql/my.cnf
  #echo "" > /etc/mysql/my.cnf
  #cat /etc/mysql/my.cnf
  #echo "begin"
  #echo "bind-address=0.0.0.0" >> /etc/mysql/my.cnf
  enter
  which mysql
  build_mysqlFiles
  echo $(date) >> result.log 
  cat ~/.mysql
  build_database
  build_tables
  run_tables
  ls --all
  #echo ${date} >> result.log 
}
test(){
if [ ! -d "subDir" ]; then
  mkdir -p "subDir"
  echo "before dont"
else
  echo "before exist"
fi
cat temp_file.out
echo $(date) > temp_file.out
cat temp_file.out
if [ -d "subDir" ]; then
    echo "exist"
else
    echo "not exist"
fi
echo $(pwd)
}
  
main
#echo 1

# docker run -itd \
#   --name mysql-test \
#   -e MYSQL_ROOT_PASSWORD=123456 \
#   -v "${HOME}"/docker_dir/mysql:/tmp/folder \
#   mysql

