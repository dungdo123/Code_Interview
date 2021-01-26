import argparse
from pathlib import Path
import os, sys
import cv2

def count_number_images(image_path):

    file_count = os.listdir(image_path)
    return len(file_count)

def combine_images(img_path_1, img_path_2, output_dir):
    num_image_1 = count_number_images(img_path_1)
    num_image_2 = count_number_images(img_path_2)
    for i in range(0, num_image_1 ):
        src_img_1 = cv2.imread(img_path_1 + "/" + f'{(os.listdir(img_path_1)[i])}')
        print(src_img_1)
        copy_img_1 = src_img_1.copy()

        # Create the file name
        save_filename = f'{i:0{8}}'  # e.g 00000069.jpg

        # Save copy images to combined directory
        combined_filename = f'{save_filename}'
        combined_path = output_dir +"/" + combined_filename
        cv2.imwrite(combined_path + '.jpg', copy_img_1)
    for j in range(0, num_image_2):
        src_img_2 =cv2.imread(img_path_2 + "/" + f'{(os.listdir(img_path_2)[j])}')
        print(src_img_2)
        copy_img_2 = src_img_2.copy()
        j = j+num_image_1
        # Create the file name
        save_filename = f'{j:0{8}}'  # e.g 00000069.jpg
        # Save copy images to combined directory
        combined_filename = f'{save_filename}'
        combined_path = output_dir + "/" + combined_filename
        cv2.imwrite(combined_path + '.jpg', copy_img_2)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="combine COCO-like datasets")
    parse.add_argument("--input_1", type=str, dest="input_1", required=True, help="path to dataset 1")
    parse.add_argument("--input_2", type=str, dest="input_2", required=True, help="path to dataset 2")
    parse.add_argument("--output_dir", type=str,dest="output_dir", required=True, help="path to output")
    args = parse.parse_args()
    sys.path.append(args.input_1)

    combine_images(args.input_1, args.input_2, args.output_dir)




