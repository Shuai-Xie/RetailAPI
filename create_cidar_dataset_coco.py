from product_cats import retail_products
from utils import build_coco_from_cates,write_json


# convert all cigar to coco datasets
if __name__ == "__main__":
    json_path = 'data/Retail Products Dataset.json'
    cigar_cates = retail_products['cigar']
    cigar_coco = build_coco_from_cates(json_path,cigar_cates,"Retail Cigar Dataset")
    write_json(cigar_coco,'data/cigar_all_coco.json')
    print('write success')