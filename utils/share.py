# -*- coding: UTF-8 -*-

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