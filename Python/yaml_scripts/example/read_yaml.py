####
# *·@Author: Wei Chen (chenwei@yusur.tech)
# *·@date: 2021-01-20 14:27:53
# *·@last_author: Wei Chen (chenwei@yusur.tech)
# *·@last_edit_time: 2021-02-03 14:53:08
####

import os
import sys
import yaml


def load_single_yml(filename):
    """加载单个yml文件
    """
    print("\n---> load single yml\n")
    with open(filename, 'r', encoding='utf-8') as fd:
        yaml_data = fd.read()
        data = yaml.load(yaml_data, Loader=yaml.FullLoader)
        print(data)
        print("data:", data["empty_str"], "type:", type(data["empty_str"]))
        print("---")
        sys.exit(0)
    

def load_multiple_yml(filename):
    """加载单个yml文件里有多个文档的情况"""
    print("\n---> load multiple yml\n")
    with open(filename, 'r', encoding='utf-8') as fd:
        yaml_data = fd.read()
        all_data = yaml.load_all(yaml_data, Loader=yaml.FullLoader)
        
        for data in all_data:
            print(data)

def print_dict(dict_t):
    for key in dict_t:
        print(key + ":", dict_t[key], "\n")
        
"""
第一种网上自制include方法
参考：https://www.cnblogs.com/robynn/p/8253783.html
"""


def yaml_include(loader, node):
    # Get the path out of the yaml file
    file_name = os.path.join(os.path.dirname(loader.name), node.value)

    with open(file_name) as inputfile:
        return yaml.load(inputfile, Loader=yaml.FullLoader)

def load_include_yml_test1(filename):
    print("\n---> load_include_yml_test1\n")
    yaml.add_constructor("!include", yaml_include)
    stream = open(filename, 'r')
    # print(yaml.load(stream))
    data = yaml.load(stream, Loader=yaml.FullLoader)

    for key in data:
        print(key, ":" , data[key], "\n")
    return data


"""
第二种网上自制include方法
参考：https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another/50987026
"""
class MyLoader(yaml.FullLoader):

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(MyLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.load(f, MyLoader)

MyLoader.add_constructor('!include', MyLoader.include)

def load_include_yml_test2(filename):
    print("\n---> load_include_yml_test2\n")
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=MyLoader)
        print_dict(data)
        return data



"""
使用pyyaml-include包
"""
from yamlinclude import YamlIncludeConstructor
YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=sys.path[0])

def use_yaml_include(filename):
    print("\n---> use_yaml_include\n")
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for key in data:
            print(key, ":", data[key], "\n")
        return data

if __name__ == "__main__":
    
    print(sys.path[0])  # 当前文件所在路径
    os.chdir(sys.path[0])
    
    filename = "single_conf.yml"
    load_single_yml(filename)

    filename = "multiple_conf.yml"
    # load_multiple_yml(filename)

    filename = "include_conf.yml"
    load_include_yml_test1(filename)
    load_include_yml_test2(filename)
    use_yaml_include(filename)