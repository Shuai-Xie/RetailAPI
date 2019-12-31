from utils.dataset_utils import get_missing_cats

'''
used to find the missing cats in product_cats.py
you should insert them to it first, then you can use other functions
'''
if __name__ == "__main__":
    json_path = 'data/Retail Products Dataset.json'
    cats = get_missing_cats(json_path)
    print(cats)
