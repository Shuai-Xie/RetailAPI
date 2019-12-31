import argparse
from utils.dataset_utils import split_coco

# Usage: train_test_split.py --orign_path data/A_coco.json --train_path data/A_train.json --test_path data/A_test.json
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = 'input a coco dataset and a train ratio, output two coco dataset as train and test'
    parser.add_argument("--origin_path", help="the path of orign coco dataset", required=True)
    parser.add_argument("--train_path", help="the path of train dataset to be saved", required=True)
    parser.add_argument("--test_path", help="the path of test dataset to be saved", required=True)
    parser.add_argument("--val_path", help="the path of val dataset to be saved", required=True)

    params = [
        '--origin_path', 'data/cigar_all_coco.json',
        '--train_path', 'data/cigar_train_coco.json',
        '--test_path', 'data/cigar_test_coco.json',
        '--val_path', 'data/cigar_val_coco.json',
    ]
    args = parser.parse_args(params)

    split_coco(args.origin_path, args.train_path, args.test_path, args.val_path)
