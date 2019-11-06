import argparse
from utils import write_json,split_coco




# Usage: train_test_split.py --orign_path data/A_coco.json --train_path data/A_train.json --test_path /data/A_test.json
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.description='input a coco dataset and a train ratio, output two coco dataset as train and test'
    parser.add_argument("--orign_path", help="the path of orign coco dataset", required=True)
    parser.add_argument("--train_path", help="the path of train dataset to be saved", required=True)
    parser.add_argument("--test_path", help="the path of test dataset to be saved",required=True)
    args = parser.parse_args()


    # json_path = "data/A_coco.json"
    split_coco(args.orign_path,args.train_path,args.test_path)