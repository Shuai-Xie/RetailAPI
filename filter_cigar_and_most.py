import json
import re
from collections import OrderedDict
from product_cats import retail_products
from utils.dataset_utils import get_most_name_list, build_coco_from_cates
from utils.io_utils import write_json

cigar_cats = retail_products['cigar']


# change the cigar name to 'A' or 'a'
def change_cigar_name(name):
    if re.match('.+_[A-Z]', name):  # 条装
        return 'A'
    else:
        return 'a'


def preprocess_samples(json_path):
    samples_dict = []

    with open(json_path, 'r', encoding='UTF-8') as fread:
        img_labels = fread.readlines()
        for line in img_labels:
            # loads: 将字符串 转化为 字典
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None:
                continue
            for idx, ann in enumerate(anns):
                cat = ann['label'][0]
                if cat in cigar_cats:
                    ann['label'][0] = change_cigar_name(cat)
                    anns[idx] = ann
            product_dict['annotation'] = anns
            samples_dict.append(product_dict)
    return samples_dict


# change the cats in cigar,just leave 'A' and 'a'
def create_product_nums_dict():
    product_dict = retail_products
    product_dict['cigar'] = ['A', 'a']
    product_nums = OrderedDict()
    for _, cats in product_dict.items():
        for cat in cats:
            product_nums[cat] = 0
    return product_nums


# build the dataset using the preprocessing data and modified product dict
def build_dataset(samples_dict, temp_path, cate_nums):
    product_nums = create_product_nums_dict()
    for product_dict in samples_dict:
        anns = product_dict['annotation']
        if anns is None:
            # print('this line has no anno:',line)
            continue
        for ann in anns:
            product_nums[ann['label'][0]] += 1  # 此类 object 数量 +1

    target_list = get_most_name_list(product_nums, cate_nums).keys()  # 获得数量最多的商品列表
    # print(target_list)
    coco_cigar_and_others = build_coco_from_cates(temp_path, target_list, "cigar and others")
    return coco_cigar_and_others


'''
an example of filter all cigar and other 3 most cats to COCO
this example uses the functions in utils
'''
if __name__ == "__main__":
    json_path = 'data/Retail Products Dataset.json'
    temp_path = 'data/temp.json'
    result_path = 'data/COCO Cigar And Others.json'
    # change the name of cigars to 'A' and 'a'
    samples = preprocess_samples(json_path)

    with open(temp_path, 'w', encoding='UTF-8') as outfile:
        for sample in samples:
            outfile.write(json.dumps(sample, ensure_ascii=False) + '\n')

    # build the dataset
    coco = build_dataset(samples, temp_path, cate_nums=5)
    write_json(coco, result_path)
