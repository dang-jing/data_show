# -*_coding:utf8-*-

import json
from PIL import Image
import base64
import os
import io
from pathlib import Path

'''# 读取json地址
jsonPath = "C:\\Users\\dangc\\Desktop\\a\\a\\"
# 写入子json地址
sonjsonpath = 'C:\\Users\\dangc\\Desktop\\a\\c\\'
#  需要截取的table
value = '题目'
# 原图地址
#   imgpath = "C:\\Users\\dangc\\Desktop\\a\\b\\"
# 截取图片存放地址
splitimg = 'C:\\Users\\dangc\\Desktop\\a\\c\\'''


class splitLabel(object):
    def __init__(self, json_Name, jsonPath, sonjsonpath, value, splitimg):
        # 读取json地址
        self.jsonPath = jsonPath
        # 写入子json地址
        self.sonjsonpath = sonjsonpath
        self.value = value
        self.splitimg = splitimg
        # 拿到当前文件名
        self.name = json_Name
        self.img_name = self.name + '.png'
        self.start()

    def start(self):
        self.get_json()
        # print(self.shapes)
        self.isValue()
        # print(self.points)
        # 遍历需要切分的位置
        if len(self.points) != 0:
            for i in range(len(self.points)):
                if '_' in self.name:
                    self.name = '{}{}{}'.format(self.name.split('_')[0], '_', i + 1)
                else:
                    self.name = '{}{}{}'.format(self.name, '_', i + 1)
                # print(self.points[i])
                point = self.points[i]
                self.split(point)
                self.set_json(point)
        else:
            print(self.name + "--------文件没有匹配的标签")

    # 写子json数据
    def set_json(self, point):
        y = point[1]
        x = point[0]
        y1 = point[3]
        x1 = point[2]
        son_shapes = []
        for i in self.shapes:
            xy = i['points']
            if self.value not in i['label']:
                xy_x = xy[0][0]
                xy_y1 = xy[0][1]
                xy_y2 = xy[1][1]
                # 判断左上点xy是否在截图的两点坐标之内
                if y - 2 < xy_y1 < y1 + 2 and x - 2 < xy_x < x1 + 2:
                    # print(x, y)
                    # print(xy)
                    # 修改标注后截取位置
                    xy[0][0] = xy[0][0] - x
                    xy[0][1] = xy_y1 - y
                    xy[1][0] = xy[1][0] - x
                    xy[1][1] = xy_y2 - y
                    son_shapes.append(i)
        self.labelme.pop('shapes')
        self.labelme['shapes'] = son_shapes
        self.labelme.pop('imageHeight')
        self.labelme.pop('imageWidth')
        self.labelme.pop('imageData')
        self.labelme['imageData'] = self.base64_str.decode('utf-8')
        img = Image.open(self.img_path)
        self.labelme['imageHeight'] = img.height
        self.labelme['imageWidth'] = img.width
        self.set()

    # 对json文件写入数据
    def set(self):
        # a = {'imageData': 'aaaaaa'}

        if not os.path.exists(self.sonjsonpath[:-1]):
            os.makedirs(self.sonjsonpath[:-1])
        data_folder = Path(self.sonjsonpath)
        file = str(data_folder / (self.name + '.json'))
        f_obj = open(file, 'w')
        json_str = json.dumps(self.labelme)
        with open(file, 'w') as json_file:
            json_file.write(json_str)
        f_obj.close()

    # 根据四点坐标切分图片
    def split(self, point):
        x = point[0]
        y = point[1]
        x1 = point[2]
        y1 = point[3]
        byte_data = base64.b64decode(self.imgdata)
        # BytesIO 对象
        image_data = io.BytesIO(byte_data)
        # 得到Image对象
        img = Image.open(image_data)
        # 裁剪图片(左，上，右，下)，笛卡尔坐标系
        img2 = img.crop((x, y, x1, y1))

        # BytesIO 对象
        imgByteArr = io.BytesIO()
        # 写入BytesIO对象
        img2.save(imgByteArr, format='PNG')
        # 获得字节
        imgByteArr = imgByteArr.getvalue()
        self.base64_str = base64.b64encode(imgByteArr)
        imgdata = base64.b64decode(self.base64_str)
        if not os.path.exists(self.splitimg[:-1]):
            os.makedirs(self.splitimg[:-1])
        data_folder = Path(self.splitimg)
        self.img_path = str(data_folder / (self.name + '.jpg'))
        with open(self.img_path, 'wb') as f:
            f.write(imgdata)

    # 拿到所有要切分的位置
    def isValue(self):
        points = []
        for i in range(len(self.shapes)):
            shapes = self.shapes[i]
            point = []
            if self.value in shapes['label']:
                a = shapes['points']
                point.append(int(a[0][0]))
                point.append(int(a[0][1]))
                point.append(int(a[1][0]))
                point.append(int(a[1][1]))
                points.append(point)
        self.points = points

    # 读取json，拿到所有数据
    def get_json(self):
        jsonx = dict()
        page = []
        data_folder = Path(self.jsonPath)
        with open(str(data_folder / (self.name + '.json')), 'r', encoding='utf-8') as path_json:  # gb18030
            jsonx = json.load(path_json)
        self.shapes = jsonx['shapes']
        self.imgdata = jsonx['imageData']
        self.labelme = jsonx


'''# 拿到路径下所有文件名
json_Name = os.listdir(r'C:\dangc\Pictures选择')
for name in json_Name:
    if 'json' in name:
        split___ = str(name).split(".")[0]
        print(split___)
splitLabel('屏幕截图2021-04-20101752', '../upload/json/', 'D:\python_project\data_show/upload/split_img/json/', '1',
           'D:\\python_project\\data_show/upload/split_img/img/')'''

# splitLabel("image1.png")
# print(os.path.exists(r"C:\Users\dangc\Desktop\a\a\0a28d2ca-c59e-11eb-8206-9c2976e90c22.json"))
