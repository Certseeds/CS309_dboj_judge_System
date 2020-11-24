hash=${1}
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
  echo "CREATE DATABASE ${hash} DEFAULT CHARACTER SET utf8mb4;" > buildDataBase.sql  
}
build_database(){
  mysql --defaults-file="${HOME}"/.mysql < buildDataBase.sql
}
build_tables(){
  mysql --defaults-file="${HOME}"/.mysql -D${hash} < createTable.sql
}
run_tables(){
  mysql --defaults-file="${HOME}"/.mysql -D${hash} < searchTable.sql > result.log
}
main(){
  enter
  build_mysqlFiles
  build_database
  build_tables
  run_tables
}
  
main
