import json
from pprint import pprint
from utils.dataset_utils import write_json
from collections import OrderedDict
from product_cats import retail_products
import os


def dict_slice(adict, start, end):
    """
    原始 dict 中 slice super_cat 字典
    adict: product_nums, OrderedDict, keys 有序
    :return: (classes, instances, OrderedDict) of a super_cat
    """
    slice_dict = OrderedDict((k, adict[k]) for k in list(adict.keys())[start:end])
    # print('slice_dict',slice_dict)
    classes = end - start
    instances = sum([num for _, num in slice_dict.items()])
    return classes, instances, slice_dict


# create the nums dict of all cats, but it's initialized zero
def create_product_nums_dict(product_dict):
    """
    :return: OrderedDict([('利群_A', 0), ('利群_a', 0), ...])
    """
    # 有序字典，key 遵从 super_cat list 顺序，顺序输出，方便查看
    # 注意 OrderedDict 虽然是有序的，但是不能 slice 截取数据
    product_nums = OrderedDict()
    for _, cats in product_dict.items():
        for cat in cats:
            product_nums[cat] = 0
    # pprint(product_nums)
    return product_nums


def parse_dataset_stats(json_path):
    dataset_stats = {
        'info': os.path.basename(json_path).replace('.json', ''),
        'images': 0,
        'classes': 0,
        'instances': 0,
        'labels': OrderedDict()  # [(super_cat, {'classes': int, 'instances': int, 'cats_num': OrderedDict()}), ...]
    }

    # 1.解析 DataTurks 导出的 标注 json 文件，存入 product_nums
    # 用 OrderedDict([('利群_A', 0), ('利群_a', 0), ...]) 方便后面累加样例数量
    product_name_dict = {'cigar': retail_products['cigar']} if 'Cigar' in json_path else retail_products
    product_nums = create_product_nums_dict(product_name_dict)

    # 避免 gbk 编码问题
    with open(json_path, 'r', encoding='UTF-8') as f:
        img_labels = f.readlines()  # each line is an image label info
        dataset_stats['images'] = len(img_labels)  # images num

        for line in img_labels:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None or len(anns) == 0:
                continue
            for ann in anns:
                if ann['label'][0] in product_nums:
                    product_nums[ann['label'][0]] += 1  # 此类 object 数量 +1

        # 2.根据 product_nums 结果 提升到父类层次结构 by slicing product_nums
        begin_idx = 0
        for super_cat, cats in product_name_dict.items():
            end_idx = begin_idx + len(cats)
            super_cat_classes, super_cat_instances, super_cat_dict = dict_slice(product_nums, begin_idx, end_idx)
            dataset_stats['labels'][super_cat] = {
                'classes': super_cat_classes,  # super_cat 子类总数
                'instances': super_cat_instances,  # super_cat 样例总数
                'labels': super_cat_dict,  # super_cat 各个 cat 样例数量, OrderedDict 存储
            }
            begin_idx = end_idx

        # 3.汇总信息，统计 classes, instances 总数
        dataset_stats['classes'] = sum([dataset_stats['labels'][s_cat]['classes'] for s_cat in product_name_dict.keys()])
        dataset_stats['instances'] = sum([dataset_stats['labels'][s_cat]['instances'] for s_cat in product_name_dict.keys()])

        return dataset_stats


# convert the json to echart need json
def cvt_echart_json(dataset_stats, out_path):
    # echart json format
    root = {
        'name': dataset_stats['info'],
        'images': dataset_stats['images'],
        'classes': dataset_stats['classes'],
        'instances': dataset_stats['instances'],
        'children': [],
    }
    for super_cat, super_cat_dict in dataset_stats['labels'].items():
        child = {
            'name': super_cat,
            'value': super_cat_dict['instances'],
            'children': [{'name': cat, 'value': num} for cat, num in super_cat_dict['labels'].items()]
        }
        root['children'].append(child)
    write_json(root, out_path)


def build_product_stats():
    # can parse Retail Product Dataset too
    data_stats = parse_dataset_stats(json_path='data/Retail Product Dataset.json')
    write_json(data_stats, out_path='data/retail_product_stats.json')
    cvt_echart_json(data_stats, out_path='data/retail_product_echart.json')


def build_cigar_stats():
    # can parse Retail Product Dataset too
    data_stats = parse_dataset_stats(json_path='data/Retail Cigar Dataset.json')
    write_json(data_stats, out_path='data/retail_cigar_stats.json')
    cvt_echart_json(data_stats, out_path='data/retail_cigar_echart.json')


if __name__ == '__main__':
    build_cigar_stats()
