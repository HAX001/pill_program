#-*- encoding=utf-8
import os
import cv2

def write_txt_to_dict(output_dir):
    output_path = os.path.join(output_dir, "output.txt")
    assert os.path.exists(output_path), "{}不存在！".format(output_path)

    all_dict = {}
    with open(output_path, "r") as f_txt:
        file_dict = {}
        for line in f_txt.readlines():
            filename, checkwell, xmin, ymin, xmax, ymax = line.split()

            im_path = os.path.join(output_dir, filename)

            im = cv2.imread(im_path)
            im_height, im_width, im_depth = im.shape


            temp_dict = {}
            temp_dict["filename"] = filename
            temp_dict["size"] = {}
            temp_dict["size"]["width"] = im_width
            temp_dict["size"]["height"] = im_height
            temp_dict["size"]["depth"] = im_depth
            temp_dict["object"] = {}
            temp_dict["object"]["bndbox"] = [[xmin, ymin, xmax, ymax]]
            temp_dict["object"]["name"] = [output_dir.split("/")[-1].split("_")[0] + "_" + checkwell]
            temp_dict["object"]["difficult"] = [0]
            if not all_dict.has_key(filename):
                # 新建
                all_dict[filename] = temp_dict
            else:
                # 添加
                all_dict[filename]["object"]["bndbox"].append(temp_dict["object"]["bndbox"][0])
                all_dict[filename]["object"]["name"].append(temp_dict["object"]["name"][0])
                all_dict[filename]["object"]["difficult"].append(temp_dict["object"]["difficult"][0])

    return all_dict