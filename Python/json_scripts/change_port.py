'''
Author: Wei Chen (chenwei@yusur.tech)
date: 2021-01-16 10:52:50
last_author: Wei Chen (chenwei@yusur.tech)
last_edit_time: 2021-01-16 10:52:51
'''
import os
import sys
import json
import yaml

global g_ignored_folders
global aim_port


def found_conf():
    pwd = os.getcwd()

    filenames = os.listdir()
    print(filenames)
    print("file num:", len(filenames))

    for fn in filenames:
        if os.path.isfile(fn):
            print("\n---> file:", fn)
            if ".json" in fn:
                change_json_port(fn)
            elif ".yml" in fn:
                change_yml_port(fn)
            else:
                print("skip current file.")
    
        elif os.path.isdir(fn):
            print("\n---> folder:", fn)
            if fn in g_ignored_folders:
                print("skip folder.")
                continue
            
            os.chdir(fn)
            found_conf()
            print("\nfound finished:", fn)
            print("back to folder:", pwd)
            os.chdir(pwd)
    
        else:
            print("\n==== DONT KNOW:", fn)
            print("pwd:", os.getcwd())


def change_json_port(fn):
    try:
        with open(fn, "r+", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

            tmp = data["server_conf"]["socket_conf"]["source_port"]
            print("raw port is:", tmp)

            data["server_conf"]["socket_conf"]["source_port"] = aim_port
            print("change port to:", aim_port)

            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile, ensure_ascii=True, indent=1)
            jsonFile.truncate()

    except Exception as e:
        raise e

def change_yml_port(fn):
    try:
        with open(fn, "r+", encoding='utf-8') as ymlFile:
            data = yaml.load(ymlFile, Loader=yaml.FullLoader)

            tmp = data["server_conf"]["socket_conf"]["source_port"]
            print("raw port is:", tmp)

            data["server_conf"]["socket_conf"]["source_port"] = aim_port
            print("change port to:", aim_port)

            ymlFile.seek(0)  # rewind
            yaml.dump(data, ymlFile, allow_unicode=True)
            ymlFile.truncate()

    except Exception as e:
        raise e

def change_port(fn):
    try:
        if ".json" in fn:
            change_json_port(fn)
        elif ".yml" in fn:
            change_yml_port(fn)

    except Exception as e:
        raise e


if __name__ == "__main__":
    global g_ignored_folders
    global aim_port

    g_ignored_folders = ["build"]
    aim_port = int(sys.argv[1])
    found_conf()