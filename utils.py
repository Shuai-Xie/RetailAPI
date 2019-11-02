import json
from collections import OrderedDict
from product_cats import retail_products

# input source file and cats, get the coco dataset
def build_coco_from_cates(json_path,target_list,info):
    coco_dataset = {
        "info": info,
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    categories = {}
    cate_id = 0
    for cate in target_list:
        category_coco = {
            "id": cate_id,
            "name": cate,
            "supercategory": "",
        }
        categories[cate] = cate_id
        coco_dataset['categories'].append(category_coco)
        cate_id += 1
    print(categories)

    with open(json_path, 'r', encoding='UTF-8') as f:
        img_labels = f.readlines()  # each line is an image label info

        pic_id = 0
        anno_id = 0
        for line in img_labels:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None or len(anns)==0:
                continue

            # 判断该图片是否包含目标类别
            checked = False
            for ann in anns:
                if ann['label'][0] in target_list:
                    checked = True
            if not checked:
                continue
            
            # 生成image信息
            img_w, img_h = anns[0]['imageWidth'], anns[0]['imageHeight']
            image = {
                'coco_url':'',
                'data_captured':'',
                'file_name':'/nfs/xs/retail' + product_dict['content'],
                'flickr_url':'',
                'id':pic_id,
                'height':img_h,
                'width':img_w,
                'license':1,
            }
            coco_dataset['images'].append(image)
            # add annotations
            for ann in anns:
                label = ann['label'][0]
                # not the correct cate ,then skip
                if not label in target_list:
                    continue
                anno_coco = {
                    "segmentation": [],
                    "area": [],
                    "iscrowd": 0,
                    "image_id": pic_id,
                    "bbox": cvt_pts2xywh(ann['points'], img_w, img_h),
                    "category_id": categories[label],
                    "id": anno_id
                }
                coco_dataset['annotations'].append(anno_coco)
                anno_id += 1
            pic_id += 1

    return coco_dataset

# convet points of bbox to (x,y,w,h) bbox
def cvt_pts2xywh(points, img_w=640, img_h=360):
    x1, y1 = pt_float2int(points[0], img_w, img_h)  # 左上
    x2, y2 = pt_float2int(points[1], img_w, img_h)  # 右上
    x3, y3 = pt_float2int(points[2], img_w, img_h)  # 右下
    x4, y4 = pt_float2int(points[3], img_w, img_h)  # 右下

    xmin, ymin = min([x1, x2, x3, x4]), min([y1, y2, y3, y4])
    xmax, ymax = max([x1, x2, x3, x4]), max([y1, y2, y3, y4])

    return [xmin, ymin, xmax - xmin, ymax - ymin]  # [x,y,w,h]    

# convert float points of image to int points in a image
def pt_float2int(pt, img_w=640, img_h=360):
    # x,y
    return max(0, min(round(pt[0] * img_w), img_w - 1)), \
           max(0, min(round(pt[1] * img_h), img_h - 1))

# write a json to a file
def write_json(adict, out_path):
    with open(out_path, 'w', encoding='UTF-8') as json_file:
        # 设置缩进，格式化多行保存; ascii False 保存中文
        json_str = json.dumps(adict, indent=2, ensure_ascii=False)
        json_file.write(json_str )

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

# create a nums dict of given cats, and all cat's names given shouldn't be modified
def get_nums_from_cats(json_path,cats):
    product_nums = OrderedDict()
    for cat in cats:
        product_nums[cat] = 0
    
    with open(json_path, 'r', encoding='UTF-8') as f:
        img_labels = f.readlines()  # each line is an image label info
        # print(len(img_labels))
        for line in img_labels:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None:
                # print('this line has no anno:',line)
                continue
            for ann in anns:
                label = ann['label'][0]
                if label in cats:
                    product_nums[label] += 1
    return product_nums

# find the missing cats in product_cats.py of given source file
def get_missing_cats(json_path):
    product_nums = create_product_nums_dict(retail_products)
    names = []

    with open(json_path, 'r', encoding='UTF-8') as f:
        img_labels = f.readlines()  # each line is an image label info
        # print(len(img_labels))
        for line in img_labels:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None:
                # print('this line has no anno:',line)
                continue
            for ann in anns:
                label = ann['label'][0]
                if label not in product_nums.keys():
                    names.append(label)
    names = list(set(names))
    return names

# given the product_nums dict, and given the most (count) cat names
def get_most_name_list(product_nums,count):
    '''
    input:
        @product_nums: the dict of products and their nums
        @count: how many product you wanna slice
        @return: the most top K products
    '''
    product_sorted = OrderedDict(sorted(product_nums.items(), key=lambda t: t[1],reverse=True))
    # print(product_sorted)
    slice_dict = OrderedDict((k, product_sorted[k]) for k in list(product_sorted.keys())[0:count])
    print(slice_dict)
    return slice_dict

# convert the json to echart need json
def cvt_echart_json(dataset_stats):
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
    write_json(root, 'data/retail_stats_echart.json')
