# -*- coding: UTF-8 -*-
import codecs
import base64
import json
from utils.es import ES
from utils import share


#   读取标注类型数据文本
def get_labels():
    label_file = codecs.open('annotation/label_config.txt', mode='r', encoding='utf-8')
    lines = label_file.readlines()
    label_file.close()
    labels = []
    for line in lines:
        if line.startswith('#'): continue
        values = line.strip().split(':')
        label_name = values[0].strip()
        label_desc = values[1].strip()
        label = dict()
        label['name'] = label_name
        label['desc'] = label_desc
        labels.append(label)
    print(labels)
    return labels


#   标注数据转labelme
def set_json(label_json, id):
    labelme = dict()
    labelme['version'] = "4.5.7"
    labelme['flags'] = dict()
    get_id = ES().get_id('original_data', id)
    labelme['imageData'] = get_id['_source']['original_json']['imageData']
    labelme['imagePath'] = "1.jpg"
    shapes = []
    for i in label_json:
        label = dict()
        splict = i.split(',')
        label['label'] = splict[-1]
        points = [[float(splict[0]), float(splict[1])], [float(splict[2]), float(splict[3])]]
        label['points'] = points
        label['group_id'] = None
        label['shape_type'] = "rectangle"
        label['flags'] = dict()
        shapes.append(label)
    labelme['shapes'] = shapes
    json_str = json.dumps(labelme, ensure_ascii=False)
    with open(r'D:\python_project\data_show\dataset\1.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


# 将图片转换成base64
def base(img_paths):
    f = open(img_paths, 'rb')
    byteC = base64.b64encode(f.read())
    # 将base64解码成字符串
    f.close()
    return byteC.decode('utf-8')


#   根据索引，页码获取数据
def match_allid(index, page):
    match_all = ES().match_all(index, page)
    return share.id_type(match_all)


#   根据索引和id返回标注信息和图片
def match_idlabel(index, id):
    get_id = ES().get_id(index, id)
    shapes_ = get_id['_source']['label']
    label = []
    label_type = []
    for i in shapes_['shapes']:
        a = []
        points_ = i['points']
        a.append(int(points_[0][0]))
        a.append(int(points_[0][1]))
        a.append(int(points_[1][0]))
        a.append(int(points_[1][1]))
        a.append(i['label'])
        label_type.append(i['label'])
        '''string = str() + ',' + str(int(points_[0][1])) + ',' + str(int(points_[1][0])) + ',' + str(
            int(points_[1][1])) + ',' + i['label']'''
        label.append(a)
    label_type = [i for n, i in enumerate(label_type) if i not in label_type[:n]]
    data = {
        "label": label,
        "data": shapes_['imageData'],
        "type": label_type
    }
    return data


#   拿到图片base64数据
def img(index, id):
    get_id = ES().get_id(index, id)
    shapes_ = get_id['_source']['original_json']
    return shapes_['imageData']


#   根据关键词搜索数据
def key_word(index,types):
    ''' a = [
        {
            "match": {
                "original_json.question_types": "解答题"
            }
        },
        {
            "match": {
                "original_json.subject_quality": "仅题目相关"
            }
        }
    ]
    ss = {'question_types': '解答题', 'subject_quality': None, 'topic_hierarchy': None, 'is_answer': None,
          'picture_type': None, 'picture_quality': None}'''
    matchs = []
    for key in types:
        if types[key]:
            match = {
                "term": {
                    key + '.keyword': types[key]
                }
            }
            matchs.append(match)
    print(matchs)
    # try:
    match = ES().multi_match(index, matchs, 1)
    '''except IndexError as e:
        print("执行")
        return {"if":False}'''
    return share.id_type(match)


if __name__ == '__main__':
    # print(ES().a())
    get_id = ES().get_id('original_data', '001f2ac4-c509-11eb-b30c-9c2976e90c1f')
    print(get_id['_source']['original_json']['imageData'])
    '''term = ES().term()
    print(term[0])
    ss = {'question_types': '你', 'subject_quality': None, 'topic_hierarchy': None, 'is_answer': None,
          'picture_type': None, 'picture_quality': None}
    key_word(ss)'''
    # match_idlabel('label_data', '46bbb25c-ded3-11eb-90b9-9c2976e90c1f')
    # print(match_allid('label_data', 1))
    '''a = ['18,241,545,307,text', '12,85,527,124,text', '21,0,603,50,text', '291,123,381,219,graph',
         '59,126,156,223,graph', '23,245,529,265,line', '32,272,429,289,line']
    set_json(a)'''
    # print(get_labels())
