hash=${1}
cputime=${2}
memory=${3}
enter(){
  echo $(pwd)
  cd /tmp/folder
  echo $(pwd)
}
build_tables(){
  echo "build_tables"
  sqlite3 ${hash}.db ""
  sqlite3 "${hash}".db < createTable.sql 
}
run_tables(){
  echo "run_tables"
  ./judge_sqlite.out "${cputime}" "${memory}" "${hash}.db"
}
main(){
  enter
  build_tables
  run_tables
}
  
main
