from product_cats import retail_products
from utils.dataset_utils import build_coco_from_cates, get_nums_from_cats, get_most_name_list
from utils.io_utils import write_json

# convert all cigar to coco datasets
if __name__ == "__main__":
    json_path = 'data/Retail Products Dataset.json'
    cigar_cates = retail_products['cigar']

    # True: filter most cigar, False: export all cigars
    filter_most = False

    if filter_most:
        cigar_nums = get_nums_from_cats(json_path, cigar_cates)
        # print('cigar_nums:', cigar_nums)
        cigar_most_nums = get_most_name_list(cigar_nums, 10)  # top cats
        cigar_cates = cigar_most_nums.keys()

    cigar_coco = build_coco_from_cates(json_path, cigar_cates, "Retail Cigar Dataset")
    write_json(cigar_coco, 'data/cigar_all_coco.json')
    print('write success')
