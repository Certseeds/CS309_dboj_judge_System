hash=${1}
cputime=${2}
memory=${3}
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
" > /tmp/.mysql
  echo "CREATE DATABASE ${hash} DEFAULT CHARACTER SET utf8mb4;" > buildDataBase.sql  
}
build_database(){
  mysql --defaults-file=/tmp/.mysql < buildDataBase.sql
}
build_tables(){
  mysql --defaults-file=/tmp/.mysql < createTable.sql
}
run_tables(){
  #g++ judge.cpp -o judge.out
  #echo $(date) >> result.log
  ./judge.out "${cputime}" "${memory}" "-D${hash}"
  # mysql --defaults-file="${HOME}"/.mysql < searchTable.sql >> result.log
  #echo $(date) >> result.log
  #cat createTable.sql >> result.log
  #cat searchTable.sql >> result.log
}
main(){
  enter
  build_mysqlFiles
  build_database
  build_tables
  run_tables
}
  
main
