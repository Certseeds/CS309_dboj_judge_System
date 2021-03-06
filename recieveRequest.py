#!/usr/bin/env python3
# coding=utf-8
import multiprocessing
from flask import Flask, request, jsonify
import json
from flask.wrappers import Response
from jsonschema.validators import validate
from dockerpyClass import MysqlDealWithObject
from dockerpySqliteClass import SqliteDealWithObject
from dockerpyPostgreClass import postgreSQLDealWithObject
from multiprocessing import Queue
import _thread
import time

app = Flask(__name__)

schema = {
    "title": "database run transfer object",
    "type": "object",
    "properties": {
        "language": {
            "type": "integer"
        },
        "createTable": {
            "type": "string"
        },
        "searchTable": {
            "type": "string"
        },
        "limitTime": {
            "type": "integer"
        },
        "limitMemory": {
            "type": "integer"
        },
    },
    "required": [
        "language", "createTable", "searchTable", "limitTime", "limitMemory"
    ]
}
# date = {"language": 1, "createTable": "", "searchTable": "", "LimitTime": 1, "limitMemory": 2}
# date2 = {"language": "", "createTable": "", "searchT


@app.route('/', methods=['POST'])
def result():
    print(time.time)
    dockerContain: MysqlDealWithObject
    try:
        data = json.loads(request.data)
    except Exception as e:
        print(e)
        return
    try:
        validate(instance=data, schema=schema)
    except Exception as e:
        print(e)
        print(type(data['createTable']))
        print(type(data['searchTable']))
        return
    languageOfDockerContain = data['language']
    try:
        if languageOfDockerContain == 0:
            dockerContain = Mysql_docker_array.get()
            while time.time() - dockerContain.initTime < 10:
                time.sleep(0.5)
                print("waiting for {} {}".format(
                    time.time(), dockerContain.initTime))
        elif languageOfDockerContain == 1:
            dockerContain = Sqlite_docker_array.get()
        elif languageOfDockerContain == 2:
            dockerContain = PostgreSQL_docker_array.get()
            while time.time() - dockerContain.initTime < 10:
                time.sleep(0.5)
                print("waiting for {} {}".format(
                    time.time(), dockerContain.initTime))
    except Exception as e:
        print(e)
        print("---队列已空---")
        return
    print(data)
    dockerContain.setvaris(data['createTable'], data['searchTable'],
                           data['limitTime'], data['limitMemory'])
    dockerContain.execCommand()
    returned = dockerContain.readResultFromFile()
    print(returned)
    return Response(returned)


def MysqlDealWithObject_write_queue(queue):
    while True:
        if queue.full():
            print("Mysql队列已满!")
        else:
            # 向队列中放入消息
            queue.put(MysqlDealWithObject("", "", 0, 0))
        time.sleep(0.5)


def dockerpySqliteClass_write_queue(queue):
    while True:
        if queue.full():
            print("Sqlite队列已满!")
        else:
            # 向队列中放入消息
            queue.put(SqliteDealWithObject("", "", 0, 0))
        time.sleep(0.5)


def dockerpyPostgreSQLClass_write_queue(queue):
    while True:
        if queue.full():
            print("postGreSQL队列已满!")
        else:
            queue.put(postgreSQLDealWithObject("", "", 0, 0))
        time.sleep(0.5)


if __name__ == "__main__":
    # 创建消息队列
    Mysql_docker_array = multiprocessing.Queue(20)
    Sqlite_docker_array = multiprocessing.Queue(20)
    PostgreSQL_docker_array = multiprocessing.Queue(20)
    # 创建子进程
    p3 = _thread.start_new_thread(
        MysqlDealWithObject_write_queue, (Mysql_docker_array,))
    p4 = _thread.start_new_thread(
        dockerpySqliteClass_write_queue, (Sqlite_docker_array,))
    p5 = _thread.start_new_thread(
        dockerpyPostgreSQLClass_write_queue, (PostgreSQL_docker_array,))
    #p1 = multiprocessing.Process(target=write_queue, args=(docker_array,))
    # 等待p1写数据进程执行结束后，再往下执行
    app.run(host='0.0.0.0')
