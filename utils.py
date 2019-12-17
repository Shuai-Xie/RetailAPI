import json, random
from collections import OrderedDict
from product_cats import retail_products


# input source file and cats, get the coco dataset
def build_coco_from_cates(json_path, target_list, info):
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

    # print("json_path:" + json_path)
    with open(json_path, 'r', encoding='UTF-8') as f:
        img_labels = f.readlines()  # each line is an image label info

        pic_id = 0
        anno_id = 0

        # print("target list:")
        # print(target_list)
        for line in img_labels:
            product_dict = json.loads(line)
            anns = product_dict['annotation']
            if anns is None or len(anns) == 0:
                continue

            # 判断该图片是否包含目标类别
            checked = False
            for ann in anns:
                if ann['label'][0] in target_list:
                    checked = True
            if not checked:
                # print('skiped:',anns[0]['label'][0])
                continue
            # print('checked:',anns[0]['label'][0])
            # 生成image信息
            img_w, img_h = anns[0]['imageWidth'], anns[0]['imageHeight']
            image = {
                'coco_url': '',
                'data_captured': '',
                'file_name': '/nfs/xs/retail' + product_dict['content'],
                'flickr_url': '',
                'id': pic_id,
                'height': img_h,
                'width': img_w,
                'license': 1,
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

# split the input coco to train and test
def split_coco(coco_path, train_path, test_path, train_ratio=0.7):
    orign = json.load(open(coco_path, 'r', encoding='UTF-8'))
    train_dataset = {}
    test_dataset = {}

    train_dataset['info'] = orign['info'] + '_test'
    train_dataset['licenses'] = orign['licenses']
    train_dataset['categories'] = orign['categories']
    train_dataset['images'] = []
    train_dataset['annotations'] = []
    test_dataset['info'] = orign['info'] + '_train'
    test_dataset['licenses'] = orign['licenses']
    test_dataset['categories'] = orign['categories']
    test_dataset['images'] = []
    test_dataset['annotations'] = []

    categories = orign['categories']
    images = orign['images']
    annotations = orign['annotations']

    dataset_size = len(images)
    train_size = int(dataset_size * train_ratio)

    cates = {}
    for category in categories:
        cates[category['name']] = category['id']

    annos = {}
    cat_images = {}
    for index, annotation in enumerate(annotations):
        if annos.get(annotation['image_id'], -1) == -1:
            annos[annotation['image_id']] = []
        if cat_images.get(annotation['category_id'], -1) == -1:
            cat_images[annotation['category_id']] = []
        annos[annotation['image_id']].append(index)
        cat_images[annotation['category_id']].append(annotation['image_id'])

    # print(cat_images)

    id_images = {}
    for image in images:
        id_images[image['id']] = image

    for (cat_id, per_cat_images) in cat_images.items():

        random.shuffle(per_cat_images)

        dataset_size = len(per_cat_images)
        train_size = int(dataset_size * train_ratio)
        train_images = per_cat_images[0:train_size]
        test_images = per_cat_images[train_size:]

        for image_id in train_images:
            train_dataset['images'].append(id_images[image_id])
            anno_indexs = annos[image_id]
            for anno_index in anno_indexs:
                if annotations[anno_index]['category_id'] == cat_id:
                    train_dataset['annotations'].append(annotations[anno_index])

        for image_id in test_images:
            test_dataset['images'].append(id_images[image_id])
            anno_indexs = annos[image_id]
            for anno_index in anno_indexs:
                if annotations[anno_index]['category_id'] == cat_id:
                    test_dataset['annotations'].append(annotations[anno_index])

    write_json(train_dataset, train_path)
    write_json(test_dataset, test_path)

# split the input coco to train and test
def split_coco_extend(coco_path, train_path, test_path, train_ratio=0.7):
    orign = json.load(open(coco_path, 'r', encoding='UTF-8'))
    train_dataset = {}
    test_dataset = {}

    train_dataset['info'] = orign['info'] + '_test'
    train_dataset['licenses'] = orign['licenses']
    train_dataset['categories'] = orign['categories']
    train_dataset['images'] = []
    train_dataset['annotations'] = []
    test_dataset['info'] = orign['info'] + '_train'
    test_dataset['licenses'] = orign['licenses']
    test_dataset['categories'] = orign['categories']
    test_dataset['images'] = []
    test_dataset['annotations'] = []

    categories = orign['categories']
    images = orign['images']
    annotations = orign['annotations']

    dataset_size = len(images)
    train_size = int(dataset_size * train_ratio)

    cates = {}
    for category in categories:
        cates[category['name']] = category['id']

    annos = {}
    for index, annotation in enumerate(annotations):
        if annos.get(annotation['image_id'], -1) == -1:
            annos[annotation['image_id']] = []
        annos[annotation['image_id']].append(index)

    # print(annos)

    random.shuffle(images)

    train_images = images[0:train_size]
    test_images = images[train_size:]
    print(len(train_images))
    print(len(test_images))

    for img in train_images:
        train_dataset['images'].append(img)
        anno_indexs = annos[img['id']]
        for anno_index in anno_indexs:
            train_dataset['annotations'].append(annotations[anno_index])

    for img in test_images:
        test_dataset['images'].append(img)
        anno_indexs = annos[img['id']]
        for anno_index in anno_indexs:
            test_dataset['annotations'].append(annotations[anno_index])

    write_json(train_dataset, train_path)
    write_json(test_dataset, test_path)

def cvt_cigar_super(coco_path, out_path):
    train_dict = json.load(open(coco_path, 'r', encoding='UTF-8'))
    categories = train_dict['categories']
    A_subs = []
    a_subs = []
    for cate in categories:
        if cate['supercategory'] == "条装":
            A_subs.append(cate['id'])
        if cate['supercategory'] == "包装":
            a_subs.append(cate['id'])

    for ann in train_dict['annotations']:
        if ann['category_id'] in A_subs:
            ann['category_id'] = 0
        elif ann['category_id'] in a_subs:
            ann['category_id'] = 1
    train_dict['categories'] = [
        {
            "id": 0,
            "name": "A"
        },
        {
            "id": 1,
            "name": "a"
        }]
    write_json(train_dict, out_path)

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
        json_file.write(json_str)


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
def get_nums_from_cats(json_path, cats):
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
def get_most_name_list(product_nums, count):
    '''
    input:
        @product_nums: the dict of products and their nums
        @count: how many product you wanna slice
        @return: the most top K products
    '''
    product_sorted = OrderedDict(sorted(product_nums.items(), key=lambda t: t[1], reverse=True))
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
