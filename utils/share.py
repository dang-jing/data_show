# -*- coding: UTF-8 -*-
import zipfile
import os
from pathlib import Path
import shutil


def id_type(match_all):
    data = []
    orgiginal = []
    for i in match_all:
        data.append(i['_id'])
        source_ = i['_source']
        original_json = dict()
        original_json['question_types'] = source_['question_types']
        original_json['subject_quality'] = source_['subject_quality']
        original_json['topic_hierarchy'] = source_['topic_hierarchy']
        original_json['is_answer'] = source_['is_answer']
        original_json['picture_type'] = source_['picture_type']
        original_json['picture_quality'] = source_['picture_quality']
        orgiginal.append(original_json)
    return {'data': data, 'original_json': orgiginal}


def zipDir(dirpath):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    split_ = dirpath.rsplit('/', 1)
    print(split_)
    data_folder = Path(dirpath)
    dirpath = str(data_folder)
    print(split_[0])
    outFullName = Path(split_[0]) / (split_[-1] + '.zip')
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    return outFullName


def unzip_file(zip_src, dst_dir):
    print(type(zip_src))
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        fz.close()
        an_garcode(dst_dir)
    else:
        print('This is not zip')

#   解决解压后中文乱码问题
def an_garcode(dir_names):
    """anti garbled code"""
    os.chdir(dir_names)

    for temp_name in os.listdir('.'):
        try:
            # 使用cp437对文件名进行解码还原
            new_name = temp_name.encode('cp437')
            # win下一般使用的是gbk编码
            new_name = new_name.decode("gbk")
            # 对乱码的文件名及文件夹名进行重命名
            os.rename(temp_name, new_name)
            # 传回重新编码的文件名给原文件名
            temp_name = new_name
        except:
            # 如果已被正确识别为utf8编码时则不需再编码
            pass

        if os.path.isdir(temp_name):
            # 对子文件夹进行递归调用
            an_garcode(temp_name)
            # 记得返回上级目录
            os.chdir('..')


def delect_path(file_path):
    #   delList = os.listdir(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        '''for f in delList:
            filePath = os.path.join(file_path, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):'''
        shutil.rmtree(file_path, True)
