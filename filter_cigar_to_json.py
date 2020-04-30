import os
import json
import re
from pprint import pprint
from collections import OrderedDict

"""
从 207 导出的 json 中选出标注中包含香烟的行
"""

data_dir = 'data'


def filter_cigars_to_json():
    in_path = os.path.join(data_dir, 'Retail Products Dataset.json')
    out_path = os.path.join(data_dir, 'Retail Cigar Dataset.json')

    with open(out_path, 'w', encoding='utf-8') as fw:
        with open(in_path, 'r', encoding='utf-8') as fr:
            lines = fr.readlines()
            print('total img:', len(lines))
            cnt = 0
            for line in lines:
                product_dict = json.loads(line)
                anns = product_dict['annotation']
                cigar_anns = []
                if anns is None:
                    continue
                # filter cigar anns from other cats
                for ann in anns:
                    cat = ann['label'][0]
                    # 要设置结尾匹配，不然 BIG_ROLL 这样也会匹配到
                    if re.match('^.+_[A-Z]$', cat) or re.match('^.+_[a-z]$', cat):
                        cigar_anns.append(ann)
                        cnt += 1
                if len(cigar_anns) > 0:
                    product_dict['annotation'] = cigar_anns
                    product_dict['extras'] = 'null'  # 防止 str 将 null 转成 None 对象
                    line = str(product_dict).replace("'", "\"") + '\n'
                    fw.write(line)
        print('cigar img:', cnt)


def descend_cat_by_num(cat_num):
    cat_list = sorted(cat_num.items(), key=lambda t: t[1], reverse=True)
    print(cat_list)
    cat_list = [c[0] for c in cat_list]
    return cat_list


def sort_dict_by_val(a_dict, descend=True):
    b_dict = OrderedDict()
    a_list = sorted(a_dict.items(), key=lambda t: t[1], reverse=descend)
    for key, value in a_list:
        b_dict[key] = value
    return b_dict


def get_cigar_cats_and_other_cats():
    # out cigar json
    in_path = os.path.join(data_dir, 'Retail Cigar Dataset.json')
    product_num = {}
    with open(in_path, 'r', encoding='UTF-8') as fr:
        lines = fr.readlines()
        for line in lines:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None:
                continue
            for ann in anns:
                cat = ann['label'][0]
                product_num[cat] = product_num.get(cat, 0) + 1  # default=0
    # print('product cats:', len(product_num))
    # product_num = sort_dict_by_val(product_num)
    # pprint(product_num)

    # divide product_num by cigars and others
    cigar_num, other_num = {}, {}
    for cat, num in product_num.items():
        # 要设置结尾匹配，不然 BIG_ROLL 这样也会匹配到
        if re.match('^.+_[A-Z]$', cat) or re.match('^.+_[a-z]$', cat):
            cigar_num[cat] = num
        else:
            other_num[cat] = num

    print('\ncigar cats:', len(cigar_num))
    cigar_num = sort_dict_by_val(cigar_num)
    pprint(cigar_num)
    print('\nother cats:', len(other_num))
    other_num = sort_dict_by_val(other_num)
    pprint(other_num)

    cigar_cats = descend_cat_by_num(cigar_num)  # str elem
    other_cats = descend_cat_by_num(other_num)
    print(','.join(cigar_cats))  # dataturks label 格式
    print(','.join(other_cats))


if __name__ == '__main__':
    filter_cigars_to_json()
    # get_cigar_cats_and_other_cats()
