# RetailAPI

General utils for annotations from [vipa-turks](https://github.com/Shuai-Xie/vipa-turks).

# Functions 

**get_all_lost_cats.py**

> get all lost cats in product_cats.py

**product_cats.py**

> all super cats and children cats of them
>
> this file should be completed when there are new cats in the source file
>
> please use **get_all_lost_cats.py** to find them

**parse_dataset_stats.py** 

> parse the source file to json file needed by echart visualization 

**create_cigar_dataset_coco.py**

> create  a coco dataset of all cigars, the classes are all cigars' class

> you can also filter the most cats in it

**filter_cigar_and_most.py**

> an example of constructing cigars and 3 other most cats
>
> the cigars are re-splited to 'A' and 'a'
>
> the total cats num can be changed in the main function
>
> the annotation num of selected cats will be printed, just change the cate_num to test it

**utils.py**

```python
# input source file and cats, get the coco dataset
def build_coco_from_cates(json_path,target_list,info)

# convet points of bbox to (x,y,w,h) bbox
def cvt_pts2xywh(points, img_w=640, img_h=360)

# convert float points of image to int points in a image
def pt_float2int(pt, img_w=640, img_h=360)

# write a json to a file
def write_json(adict, out_path)

# create the nums dict of all cats, but it's initialized zero
def create_product_nums_dict(product_dict)

# create a nums dict of given cats, and all cat's names given shouldn't be modified
def get_nums_from_cats(json_path,cats)

# find the missing cats in product_cats.py of given source file
def get_missing_cats(json_path)

# given the product_nums dict, and given the most (count) cat names
def get_most_name_list(product_nums,count)

# convert the json to echart need json
def cvt_echart_json(dataset_stats)
```


## todo [Functions]