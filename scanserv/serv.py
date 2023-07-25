import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from scanserv import ( success,fail)

bp = Blueprint('serv', __name__, url_prefix='/serv')



# 扫描文件返回文件路径
@bp.route('/scan', methods=('GET', 'POST'))
def scan():
    return render_template("scan.html")
       

@bp.route('/do_scan', methods=('GET', 'POST'))
def do_scan():
    time.sleep(2)
    return success({"path":"/static/assets/sample.jpg"})

@bp.route('/print', methods=('GET', 'POST'))
def print():
    return render_template("print.html")