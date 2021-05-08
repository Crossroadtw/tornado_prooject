# Tornado项目介绍

**PS:之前的代码虽然也整理了，但还是有些数据暴露了，就设置私有了，这次吸取教训重新规划了项目结构**


## 项目依赖/介绍
* 基于`pipenv`的虚拟环境
* 前后端不分离项目
* 尝试tornado的多线程+协程的异步开发模式

## 项目初始化
* 数据库依赖：redis、mongodb均无密码
* 邮件依赖：163邮箱（qq邮箱可以实现异步发送，163不支持tls，这块没细看）
* 修改配置文件:复制->项目/config/conf_demo.yaml->项目/config/conf.yaml->填入自己的配置
* 项目运行后，登录的话没有注册接口在：项目/model_conf/mongo_model中查看结构直接调用方法插入数据
### 有pipenv环境
* pipenv sync 
* pipenv shell 
* python app.py
* 运行成功
 
### 无pipenv环境
* pip导出包：pip freeze >requirements.txt
* pip导入包：pip install -r requirements.txt
* python app.py
* 运行成功
