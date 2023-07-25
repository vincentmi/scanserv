import os
import configparser
from flask import (Flask,render_template )
import datetime


def success(data):
    return {
        "code":0,
        "message":"ok",
        "data":data
    }
    
def fail(code=500,message="server error",data=None):
    return {
        "code":code,
        "message":message,
        "data":data
    }


def create_app(test_config=None):
    # 创建Flask对象，设置加载
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # 加载配置文件
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 加载测试配置
        app.config.from_mapping(test_config)
    
    # 注册蓝图
    app.add_url_rule('/', endpoint='welcome')
    
    from . import serv
    app.register_blueprint(serv.bp)
    
    from . import fileman
    app.register_blueprint(fileman.bp)

    # 注册一个简单的路由
    @app.route('/info')
    def info():
        info = {
            "name":"scanserv",
            "description":"a web ui for printer and scaner",
            "author" :"miwenshu@gmail.com",
            "version":"1.0.0",
            "t": datetime.datetime.now().timestamp()
        }
        return success(info)
    
    @app.route('/welcome')
    def welcome():
        return render_template("welcome.html")

    return app