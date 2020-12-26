#!/usr/bin/env python3
# coding=utf-8
import os
import time
from ntpath import expanduser
from os import error, times, urandom
from pathlib import Path
from shutil import copyfile
from typing import Any
import random
import string
import docker
from docker.api.client import APIClient
from docker.client import DockerClient
import os
import sys
import stat
import json
client: DockerClient
clientAPI: APIClient


def get_random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


client = docker.from_env()
clientAPI = docker.from_env().api


class postgreSQLDealWithObject(object):
    """
    docstring
    """

    def setvaris(self, create: str, search: str, maxTime: int, maxMemory: int):
        self.create = "{}".format(create)
        self.search = "{}".format(search)
        self.maxTime = maxTime
        self.maxMemory = maxMemory
        self.createFileAndFolder()

    def __init__(self, create: str, search: str, maxTime: int, maxMemory: int):
        self.folderName = get_random_string(8)
        self.create = create
        self.search = search
        self.maxTime = maxTime
        self.maxMemory = maxMemory
        print(self.folderName)
        self.createFileAndFolder()
        self.createAndPrepareImage()
        self.initTime = time.time()

    def createFileAndFolder(self) -> None:
        publicPath = "/home/nanoseeds/docker_dir/"
        publicPath2 = "/home/nanoseeds/docker_dir/postgreSQLTemp/{}/".format(
            self.folderName)
        if not os.path.exists(publicPath2):
            os.mkdir(publicPath2)
        self.cpp_file=""
        with open("/home/nanoseeds/docker_dir/postgreSQL/judge_psql.cpp", 'r+') as file:
            self.cpp_file = file.read()
        # Path("{}{}".format(publicPath2, "buildDataBase.sql")).touch()
        Path("{}{}".format(publicPath2, "createTable.sql")).touch()
        Path("{}{}".format(publicPath2, "judge_psql.out")).touch()
        Path("{}{}".format(publicPath2, "judge_psql.cpp")).touch()
        Path("{}{}".format(publicPath2, "searchTable.sql")).touch()
        Path("{}{}".format(publicPath2, "result.log")).touch()
        Path("{}{}".format(publicPath2, "cputime")).touch()
        Path("{}{}".format(publicPath2, "memoryCost")).touch()
        Path("{}{}".format(publicPath2, "state")).touch()
        # with open("{}{}".format(publicPath2, "buildDataBase.sql"), mode='r+') as file:
        #     file.write(
        #         "CREATE DATABASE {} DEFAULT CHARACTER SET utf8mb4;".format(self.folderName))
        with open("{}{}".format(publicPath2, "createTable.sql"), mode='r+') as file:
            file.write(self.create)
        with open("{}{}".format(publicPath2, "searchTable.sql"), mode='r+') as file:
            file.write(self.search)
        with open("{}{}".format(publicPath2,"judge_psql.cpp"), mode='r+') as file:
            file.write(self.cpp_file)
        copyfile("{}{}".format(publicPath, "postgreSQL/script.sh"),
                 "{}{}".format(publicPath2, "script.sh"))
        os.chmod("{}{}".format(publicPath2, "script.sh"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        os.chmod("{}{}".format(publicPath2, "judge_psql.out"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        os.chmod("{}{}".format(publicPath2, "cputime"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        os.chmod("{}{}".format(publicPath2, "memoryCost"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        os.chmod("{}{}".format(publicPath2, "state"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
        os.chmod("{}{}".format(publicPath2, "result.log"),
                 stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
    def createAndPrepareImage(self) -> None:
        self.docker_id = clientAPI.create_container(
            # user="1000",
            image="frodenas/postgresql",
            detach=True,
            name=self.folderName,
            environment={"POSTGRES_USERNAME": "myuser",
                         "POSTGRES_PASSWORD": "mypassword",
                         "POSTGRES_DBNAME": "mydb"},
            # ports=[3306],  # inside ports
            volumes=['/tmp/folder'],
            host_config=clientAPI.create_host_config(
                # port_bindings={3306: 3310},
                binds={"/home/nanoseeds/docker_dir/postgreSQLTemp/{}/".format(self.folderName): {
                    'bind': '/tmp/folder',
                    'mode': 'rw'
                }}
            )
        )
        clientAPI.start(self.docker_id['Id'])

    def execCommand(self) -> None:
        clientAPI.exec_start(
            clientAPI.exec_create(
                container=self.folderName,
                user="postgres",
                cmd="/bin/bash /tmp/folder/script.sh {} {} {} > build.log".format(
                    self.folderName, str(self.maxTime), str(self.maxMemory))
            )
        )
        self.stopAndRemove(self.folderName)

    def stopAndRemove(self, id: str) -> None:
        clientAPI.stop(container=id, timeout=10)
        clientAPI.remove_container(container=id)

    def readResultFromFile(self) -> str:
        with open("/home/nanoseeds/docker_dir/postgreSQLTemp/{}/result.log".format(self.folderName), mode='r') as file:
            will_return = file.read()
        with open("/home/nanoseeds/docker_dir/postgreSQLTemp/{}/cputime".format(self.folderName), mode='r') as file:
            cputime = int(file.read())
        with open("/home/nanoseeds/docker_dir/postgreSQLTemp/{}/memoryCost".format(self.folderName), mode='r') as file:
            memory = int(file.read())
        with open("/home/nanoseeds/docker_dir/postgreSQLTemp/{}/state".format(self.folderName), mode='r') as file:
            state = int(file.read())
        jsonReturn = {'data': will_return,
                      'time': cputime,
                      'memory': memory,
                      'state': state}
        return json.dumps(jsonReturn)


if __name__ == "__main__":
    createTable = ""
    with open("./postgreSQL/createTable.sql", 'r+') as file:
        createTable = file.read()
    searchTable = ""
    with open("./postgreSQL/searchTable.sql", 'r+') as file:
        searchTable = file.read()
    cpp_file = ""
    with open("./postgreSQL/judge_psql.cpp", 'r+') as file:
        cpp_file = file.read()
    test = postgreSQLDealWithObject('', '', 3, 1025000)
    test.setvaris(createTable, searchTable, 3, 1024000)
    with open("{}{}".format("/home/nanoseeds/docker_dir/postgreSQLTemp/{}/".format(test.folderName), "judge_psql.cpp"), mode='r+') as file:
        file.write(cpp_file)
    time.sleep(10)
    print("/bin/bash /tmp/folder/script.sh {} {} {}".format(
        test.folderName, str(test.maxTime), str(test.maxMemory)))
    test.execCommand()
    # print(test.readResultFromFile())
