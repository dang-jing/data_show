# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, render_template, request, send_file
from utils.es import ES
from flask_cors import *
import os
from utils import tool
import json
from fileapp import file_bp

app = Flask(__name__)
es = ES()
app.register_blueprint(file_bp,url_prefix='/file')

@app.route('/match/')
def match_all():
    page = request.args.get('page')
    match_all = es.match_all('original_data', page)
    data = []
    for i in match_all:
        data.append(i['_id'])
        '''json_ = i['_source']['original_json']
        #删除指定key值
        del json_['imageData']'''
    return jsonify(dict({'data': data}))


@app.route('/all_label')
def matchall_label():
    index = request.args.get('index')
    page = request.args.get('page')
    data = tool.match_allid(index, page)
    return jsonify(data)


# @app.route('/img/<img_id>')
@app.route('/img')
def img():
    # data:;base64,
    # img_id = '001f2ac4-c509-11eb-b30c-9c2976e90c1f'
    # data = es.get_id(img_id)
    id = request.args.get('id')
    data = tool.match_idlabel('label_data', id)
    # img_data = data['_source']['original_json']['imageData']
    # 返回base64数据图片给页面img.html
    # return render_template('img.html', img_stream=data, img_id='1')
    return jsonify(data)


@app.route('/label_img')
def label_img():
    id = request.args.get('id')
    data = tool.img('original_data', id)
    return jsonify({'data': data})


'''
# 读取标注图片
@app.route('/api/annotation/sample', methods=['GET'])
def get_labels():
    if 'index' in request.args:
        img_name = request.args['index'] + '.jpg'
        img_path = os.path.join('./dataset', img_name)
        return send_file(img_path, mimetype='application/octet-stream',
                         as_attachment=True, attachment_filename=img_name)
    else:
        result = dict()
        result['message'] = 'failure'
        return jsonify(result)
        '''


# 读取类别标签
@app.route('/api/annotation/labels', methods=['GET'])
def get_sample():
    label_json = tool.get_labels()
    result = dict()
    result['message'] = 'success'
    result['data'] = label_json
    return jsonify(result)


#   提交标注数据
@app.route('/api/pust', methods=['GET'])
def pust():
    label_json = request.args.getlist('label_json[]')
    get_id = request.args.get('id')

    # label_json=request.args.getlist('label_json')
    # request.args['label_js)on']
    tool.set_json(label_json, get_id)
    return jsonify({'a': 'aa'})


#   关键词搜索数据
@app.route('/keyword', methods=['POST'])
def keyword():
    get = request.values['data']
    index = request.form.get('index')
    # type_ = request.files['picture_type']
    # print(type_)
    print(index)
    return tool.key_word(index, json.loads(get))


if __name__ == '__main__':
    try:
        # 解决跨域问题
        CORS(app, supports_credentials=True)
        # 运行调试服务器
        app.run(host='0.0.0.0', port=8080, debug=False)
    except:
        pass
    # print(ES().get_id('001f2ac4-c509-11eb-b30c-9c2976e90c1f'))
    # print(ES().match_all())
    # match_all()
