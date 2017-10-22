# -*- encoding=utf-8
import os
import random

if __name__ == "__main__":
    annotation_path = os.path.join(os.path.dirname(__file__), "Annotations")
    assert os.path.exists(annotation_path), "{}不存在！".format(annotation_path)
    JPEGImage_path = os.path.join(os.path.dirname(__file__), "JPEGImages")
    assert os.path.exists(JPEGImage_path), "{}不存在！".format(JPEGImage_path)
    Imageset_path = os.path.join(os.path.dirname(__file__), "Imagesets")
    assert os.path.exists(Imageset_path)

    list_a = os.listdir(annotation_path)
    list_j = os.listdir(JPEGImage_path)

    assert len(list_a) == len(list_j), "好好查查Annotations和JPEGImage文件夹下的数据是否对应！！！"

    l = []
    for j in list_j:
        name = j.split(".")[0]
        l.append(name)

    #对l索引进行随机处理
    r = random.sample(l, len(l))
    train_step = int(len(l) * 0.6)
    test_step = int(len(l) * 0.9)

    #train.txt
    tr = r[:train_step]
    with open(os.path.join(Imageset_path, "train.txt"), "w") as f_tr:
        for text in tr:
            f_tr.write(text + "\n")

    #test.txt
    te = r[train_step:test_step]
    with open(os.path.join(Imageset_path, "test.txt"), "w") as f_te:
        for text in te:
            f_te.write(text + "\n")

    #val.txt
    va = r[test_step:]
    with open(os.path.join(Imageset_path, "val.txt"), "w") as f_va:
        for text in va:
            f_va.write(text + "\n")

    print("Imageset完成！")