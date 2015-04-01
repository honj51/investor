# Investor 
还在开发中,会有更多的功能加入!

## 目前的功能

- 爬取网贷系统 （Octopus）
- 实时显示数据  （eagle）

## 依赖

- Python 2.7+
- Scrapy  0.24.4
- Redis 2.8+
- redis-py  2.10.3
- socket.io 1.3.5
- node_redis 0.12.1
- Express  4.12.3
- Angularjs 1.3.15
- Bootstrap 3.3.4

## 安装

在根目录下运行下面的命令安装python的依赖包:

    pip install -r requirements.txt
    
在eagle目录下运行下面的命令安装JS依赖包:

    npm install
    bower install angularjs bootstrap


## FAQ

**No package 'libffi' found**

    sudo yum install libffi libffi-devel 

**ERROR: /bin/sh: xslt-config: command not found**

    sudo yum install libxml2-devel libxslt-devel

