import json, random
from utils.box_utils import *
from utils.io_utils import load_json, write_json
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
    # print(categories)

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
                    "segmentation": cvt_poly_fpts_to_segmentation(ann['points'], img_w, img_h),  # add polygon segmentation
                    "area": cal_area(ann['points'], img_w, img_h),  # add area
                    "iscrowd": 0,
                    "image_id": pic_id,
                    "bbox": cvt_rect_fpts_to_xywh(ann['points'], img_w, img_h),
                    "category_id": categories[label],
                    "id": anno_id
                }
                coco_dataset['annotations'].append(anno_coco)
                anno_id += 1
            pic_id += 1

    return coco_dataset


# split the input coco to train and test
def split_coco(coco_path, train_path, test_path, val_path,
               train_ratio=0.7, val_ratio=0.3):
    origin = load_json(coco_path)
    train_dataset = {}
    test_dataset = {}
    val_dataset = {}

    train_dataset['info'] = origin['info'] + '_train'
    test_dataset['info'] = origin['info'] + '_test'
    val_dataset['info'] = origin['info'] + '_val'

    train_dataset['licenses'] = test_dataset['licenses'] = val_dataset['licenses'] = origin['licenses']
    train_dataset['categories'] = test_dataset['categories'] = val_dataset['categories'] = origin['categories']
    train_dataset['images'] = []
    test_dataset['images'] = []
    val_dataset['images'] = []
    train_dataset['annotations'] = []
    test_dataset['annotations'] = []
    val_dataset['annotations'] = []

    images = origin['images']
    annotations = origin['annotations']

    annos = {}  # dict { image_id : anns idx }
    cat_images = {}  # dict { cat_id: image_ids }
    for index, annotation in enumerate(annotations):
        if annos.get(annotation['image_id'], -1) == -1:
            annos[annotation['image_id']] = []  # create ann image_id key
        if cat_images.get(annotation['category_id'], -1) == -1:
            cat_images[annotation['category_id']] = []  # create cat image_id key
        annos[annotation['image_id']].append(index)
        cat_images[annotation['category_id']].append(annotation['image_id'])

    id_images = {}  # dict { image_id: image_dict }
    for image in images:
        id_images[image['id']] = image

    for (cat_id, per_cat_images) in cat_images.items():  # each cat split

        random.shuffle(per_cat_images)

        dataset_size = len(per_cat_images)
        train_size = int(dataset_size * train_ratio)
        val_size = int(dataset_size * val_ratio)
        train_images = per_cat_images[0:train_size]
        test_images = per_cat_images[train_size:]

        # add val
        val_from_train = int(val_size * train_ratio)
        val_from_test = val_size - val_from_train
        val_images = random.sample(train_images, val_from_train) + random.sample(test_images, val_from_test)

        for image_id in train_images:
            train_dataset['images'].append(id_images[image_id])
            anno_indexs = annos[image_id]  # anns in an img
            for anno_index in anno_indexs:
                if annotations[anno_index]['category_id'] == cat_id:  # judge cat id of anns in an img
                    train_dataset['annotations'].append(annotations[anno_index])

        for image_id in test_images:
            test_dataset['images'].append(id_images[image_id])
            anno_indexs = annos[image_id]
            for anno_index in anno_indexs:
                if annotations[anno_index]['category_id'] == cat_id:
                    test_dataset['annotations'].append(annotations[anno_index])

        for image_id in val_images:
            val_dataset['images'].append(id_images[image_id])
            anno_indexs = annos[image_id]
            for anno_index in anno_indexs:
                if annotations[anno_index]['category_id'] == cat_id:
                    val_dataset['annotations'].append(annotations[anno_index])

    write_json(train_dataset, train_path)
    write_json(test_dataset, test_path)
    write_json(val_dataset, val_path)


# split the input coco to train/val/test
def split_coco_extend(coco_path, train_path, test_path, val_path,
                      train_ratio=0.7, val_ratio=0.3):
    origin = json.load(open(coco_path, 'r', encoding='UTF-8'))
    train_dataset = {}
    test_dataset = {}
    val_dataset = {}

    train_dataset['info'] = origin['info'] + '_train'
    test_dataset['info'] = origin['info'] + '_test'
    val_dataset['info'] = origin['info'] + '_val'

    train_dataset['licenses'] = test_dataset['licenses'] = val_dataset['licenses'] = origin['licenses']
    train_dataset['categories'] = test_dataset['categories'] = val_dataset['categories'] = origin['categories']
    train_dataset['images'] = []
    test_dataset['images'] = []
    val_dataset['images'] = []
    train_dataset['annotations'] = []
    test_dataset['annotations'] = []
    val_dataset['annotations'] = []

    images = origin['images']
    annotations = origin['annotations']

    dataset_size = len(images)
    train_size = int(dataset_size * train_ratio)
    val_size = int(dataset_size * val_ratio)

    # dict { image_id : anns idx }
    annos = {}  # key: image_id; val: [ann indx in annotations]
    for index, annotation in enumerate(annotations):
        if annos.get(annotation['image_id'], -1) == -1:
            annos[annotation['image_id']] = []  # create key:[]
        annos[annotation['image_id']].append(index)

    random.shuffle(images)

    train_images = images[0:train_size]
    test_images = images[train_size:]

    # add val
    val_from_train = int(val_size * train_ratio)
    val_from_test = val_size - val_from_train
    val_images = random.sample(train_images, val_from_train) + random.sample(test_images, val_from_test)

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

    for img in val_images:
        val_dataset['images'].append(img)
        anno_indexs = annos[img['id']]
        for anno_index in anno_indexs:
            val_dataset['annotations'].append(annotations[anno_index])

    write_json(train_dataset, train_path)
    write_json(test_dataset, test_path)
    write_json(val_dataset, val_path)


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
        {"id": 0, "name": "A"},
        {"id": 1, "name": "a"}
    ]
    write_json(train_dict, out_path)


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
