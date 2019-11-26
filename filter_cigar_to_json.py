import os
import json
import re
from pprint import pprint

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
                if anns is None:
                    continue
                has_cigar = False
                for ann in anns:
                    cat = ann['label'][0]
                    if re.match('.+_[A-Z]', cat) or re.match('.+_[a-z]', cat):
                        has_cigar = True
                        cnt += 1
                        break
                if has_cigar:
                    fw.write(line)
        print('cigar img:', cnt)


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
    print('product cats:', len(product_num))
    pprint(product_num)

    # divide product_num by cigars and others
    cigar_num, other_num = {}, {}
    for cat, num in product_num.items():
        if re.match('.+_[A-Z]', cat) or re.match('.+_[a-z]', cat):
            cigar_num[cat] = num
        else:
            other_num[cat] = num

    print('\ncigar cats:', len(cigar_num))
    pprint(cigar_num)
    print('\nother cats:', len(other_num))
    pprint(other_num)


if __name__ == '__main__':
    # filter_cigars_to_json()
    get_cigar_cats_and_other_cats()
