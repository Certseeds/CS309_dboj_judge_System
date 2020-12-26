#!/bin/bash
set pipefail
hash=${1}
cputime=${2}
memory=${3}
enter(){
  sudo -u postgres -i
  echo $(pwd)
  cd /tmp/folder
  echo $(pwd)
}
build_tables(){
 psql < createTable.sql
}
run_tables(){
  g++ -std=c++11  judge_psql.cpp -o judge_psql.out  
  #g++ judge.cpp -o judge.out
  #echo $(date) >> result.log
  psql < searchTable.sql
  ./judge_psql.out "${cputime}" "${memory}" "-D${hash}"
  # mysql --defaults-file="${HOME}"/.mysql < searchTable.sql >> result.log
  #echo $(date) >> result.log
  #cat createTable.sql >> result.log
  #cat searchTable.sql >> result.log
  cat ./result.log
}
main(){
  enter
  build_tables
  run_tables
}
  
main
