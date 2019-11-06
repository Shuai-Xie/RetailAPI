from product_cats import retail_products
from utils import get_nums_from_cats,get_most_name_list,build_coco_from_cates,write_json
import re

def split(cigar_cats):
    A = []
    a = []
    for cat in cigar_cats:
        if re.match('.+_[A-Z]',cat):
            A.append(cat)
        else:
            a.append(cat)
    return A,a


if __name__ == "__main__":
    json_path = 'data/Retail Products Dataset.json'
    cigar_cats = retail_products['cigar']
    print(cigar_cats)
    A,a = split(cigar_cats)
    A_nums = get_nums_from_cats(json_path,A)
    a_nums = get_nums_from_cats(json_path,a)

    A_most_nums = get_most_name_list(A_nums,10)
    a_most_nums = get_most_name_list(a_nums,10)
    A_cates = A_most_nums.keys()
    a_cates = a_most_nums.keys()
    
    A_coco = build_coco_from_cates(json_path,A_cates,"most A coco")
    a_coco = build_coco_from_cates(json_path,a_cates,"most a coco")

    write_json(A_coco,'data/A_coco.json')
    write_json(a_coco,'data/a_coco.json')