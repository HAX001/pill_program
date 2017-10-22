# -*- encoding=utf-8
import os
import wrape_white_pills as white
import wrape_blue_pills as blue
import wrape_yellow_pills as yellow
import wrape_oill_pills as oill

from txt_to_dict import write_txt_to_dict
from dict_to_xml import write_dict_to_xml

def process(path, annotation_path, JPEGImage_path):
    list_annotation = os.listdir(annotation_path)
    list_JPEGImage = os.listdir(JPEGImage_path)
    assert len(list_annotation) == len(list_JPEGImage),\
        "查查{}和{}路径下的文件数是否相等！".format(annotation_path, JPEGImage_path)
    # 读取output.txt文件，变成dict字典
    all_dict = write_txt_to_dict(path)

    # 进行annotation和JPEGImage步骤
    for k, v in all_dict.items():
        # 新加的文件序号得接在原来文件的序号后面
        k_int = int(k.split(".")[0]) + len(list_annotation)

        # 生成相应的xml文件到Imagesets目录
        filename_path = os.path.join(annotation_path, "{:06d}".format(k_int) + ".xml")
        v["filename"] = "{:06d}.jpg".format(k_int)
        write_dict_to_xml(v, filename_path)
        # 剪切相应的图像到JPEGImage目录,同时修改名字
        image_origin_filename = os.path.join(path, k)
        image_target_filename = os.path.join(JPEGImage_path, "{:06d}".format(k_int) + ".jpg")
        os.rename(image_origin_filename, image_target_filename)

    # 删除output.txt
    os.remove(os.path.join(path, "output.txt"))
    # 并将剩余图像重新排序
    list_last = os.listdir(path)
    for i in range(len(list_last)):
        old_name_path = os.path.join(path, list_last[i])
        new_name_path = os.path.join(path, "{:06d}".format(i+1) + ".jpg")
        os.rename(old_name_path, new_name_path)

    print("{} 注释完成！".format(path))


if __name__ == "__main__":
    #先判断annotation文件夹和JPFGImage文件夹下的文件数是否相等
    annotation_path = os.path.join(os.path.dirname(__file__), "Annotations")
    assert os.path.exists(annotation_path), "{}不存在！".format(annotation_path)
    JPEGImage_path = os.path.join(os.path.dirname(__file__), "JPEGImages")
    assert os.path.exists(JPEGImage_path), "{}不存在！".format(JPEGImage_path)



    # 获取相应的标注过的图像路径
    white_path = white._get_write_to_path()
    blue_path = blue._get_write_to_path()
    yellow_path = yellow._get_write_to_path()
    oill_path = oill._get_write_to_path()

    # 判断是否有需要annotation，即：有无output.txt文件
    if os.path.exists(os.path.join(white_path, "output.txt")):
        process(white_path, annotation_path, JPEGImage_path)
    else:
        print("{} 无标注文件！".format(white_path))

    if os.path.exists(os.path.join(blue_path, "output.txt")):
        process(blue_path, annotation_path, JPEGImage_path)
    else:
        print("{} 无标注文件！".format(blue_path))

    if os.path.exists(os.path.join(yellow_path, "output.txt")):
        process(yellow_path, annotation_path, JPEGImage_path)
    else:
        print("{} 无标注文件！".format(yellow_path))

    if os.path.exists(os.path.join(oill_path, "output.txt")):
        process(oill_path, annotation_path, JPEGImage_path)
    else:
        print("{} 无标注文件！".format(oill_path))

    print("annotation完成！")