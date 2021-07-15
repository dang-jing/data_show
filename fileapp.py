# -*- coding: UTF-8 -*-

from flask import Flask, Blueprint, request, send_from_directory, make_response, Response
import os
from utils import tool
from utils import share

file_bp = Blueprint('file', __name__)


@file_bp.route('/split', methods=["POST", "GET"])
def file_split():
    file = request.files.get("filename")
    value = request.form.get('txt')
    file_type = request.form.get('file_type')
    print(file,value,file_type)
    '''print(value)
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    print("获取上传文件的名称为[%s]\n" % file_name)
    file_path = os.path.dirname(__file__) + '/upload/json/' + file_name
    file.save(file_path)  # 保存文件

    store_path = tool.split_img(file_path, value)

    #   流下载
    def send_file():
        with open(store_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
                if not data:
                    break
                yield data

    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename={}'.format(
        file_name.encode().decode('latin-1'))  # 如果不加上这行代码，导致下图的问题

    return response'''
    return ''


@file_bp.route('/ccc', methods=["GET", "POST"])
def a():
    filename = '屏幕截图2021-04-20101752.json'
    '''response = make_response(
        send_from_directory(os.path.dirname(__file__) + '/upload/',
                            filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response'''

    def send_file():
        store_path = os.path.dirname(__file__) + '/upload/' + filename
        with open(store_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
                if not data:
                    break
                yield data

    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename={}'.format(
        filename.encode().decode('latin-1'))  # 如果不加上这行代码，导致下图的问题
    return response
