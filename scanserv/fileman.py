import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from scanserv import ( success,fail)

bp = Blueprint('fileman', __name__, url_prefix='/fileman')

fileman_path = "/Users/vincentmi/work/python/scanserv/scanserv/static"
fileman_url="/static"


def file_can_delete(file):
    print("Can_delete_"+file)
    if file.startswith('/files') or file.startswith('/upfiles'):
        return True
    else:
        return False
    
    
def is_valid(path):
    dir = path.lstrip("/")
    
    dir_parts = [] 
    path_nav = []
    
    for i in dir.split("/"):
        if i == "." or i=='..':
            return False
    
    return True
        


@bp.route('/view', methods=('GET', 'POST'))
def index():
    return render_template("fileman_view.html")
    



@bp.route('/delete', methods=('GET', 'POST'))
def delete():
    #delete  
    path = request.args["path"]
    print(path)
    if (not is_valid(path)) or (not file_can_delete(path)):
        return fail("无效的路径")
    r_path = fileman_path+"/"+path
    
    print(r_path)
    
    if os.path.isfile(r_path) : 
        if os.unlink(r_path):
            return success("ok")
    
    return fail()
    
        

# 扫描文件返回文件路径
@bp.route('/list', methods=('GET', 'POST'))
def list(dir="/"):
    dir = request.args["dir"]
    
    dir = dir.lstrip("/")
    
    dir_parts = [] 
    
    path_nav = []
    
    for i in dir.split("/"):
        if i == "." or i=='..':
            return fail("无效的路径")
        dir_parts.append(i)
        
        path_nav.append({"name":i,"path":"/".join(dir_parts)})
        
        
    dir = "/".join(dir_parts)

    
    if(dir == ""):
        req_path = fileman_path
    else:
        req_path =  fileman_path +"/"+ dir
        

    print(req_path)
    file_list = []
    for filename in os.listdir(req_path):
        if filename == "." :
            continue
        path = req_path+"/"+filename
        relative_path = path.replace(fileman_path,"")
        url = fileman_url+"/"+relative_path
        if os.path.isfile(path):
            file_list.append({"path":relative_path , "url":url , "is_file": True , "name":filename , "can_delete": file_can_delete(relative_path)})
        else:
            file_list.append({"path":relative_path , "url":url , "is_file": False, "name":filename , "can_delete":False})
    
    return success({ "root":dir,"file_list":file_list,"nav_list":path_nav})

