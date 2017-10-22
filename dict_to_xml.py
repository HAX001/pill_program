# -*- encoding=utf-8
from pprint import pprint
from xml.dom.minidom import Document


def write_dict_to_xml(mydict, filename):
    """
    :param mydict: 需被转化的字典
    :param filename: 目标文件名
    :return:
    用来完成从一个字典到.xml文件的转化，被调用时要注意配合使用，可修改！
    """
    doc = Document()

    annotationlist = doc.createElement("annotation")

    doc.appendChild(annotationlist)

    for (k, v) in mydict.iteritems():
        if k == "object":
            for i in range(len(v["bndbox"])):

                obj = doc.createElement("object")
                annotationlist.appendChild(obj)
                # ***
                bdb = doc.createElement("bndbox")
                obj.appendChild(bdb)

                x_min = doc.createElement("xmin")
                x_min_text = doc.createTextNode(str(v["bndbox"][i][0]))
                x_min.appendChild(x_min_text)
                bdb.appendChild(x_min)

                y_min = doc.createElement("ymin")
                y_min_text = doc.createTextNode(str(v["bndbox"][i][1]))
                y_min.appendChild(y_min_text)
                bdb.appendChild(y_min)

                x_max = doc.createElement("xmax")
                x_max_text = doc.createTextNode(str(v["bndbox"][i][2]))
                x_max.appendChild(x_max_text)
                bdb.appendChild(x_max)

                y_max = doc.createElement("ymax")
                y_max_text = doc.createTextNode(str(v["bndbox"][i][3]))
                y_max.appendChild(y_max_text)
                bdb.appendChild(y_max)
                # ****
                name = doc.createElement("name")
                name_text = doc.createTextNode(str(v["name"][i]))
                name.appendChild(name_text)
                obj.appendChild(name)

                diff = doc.createElement("diffcult")
                diff_text = doc.createTextNode(str(0))
                diff.appendChild(diff_text)
                obj.appendChild(diff)

        if k == "size":
            si = doc.createElement("size")
            annotationlist.appendChild(si)

            width = doc.createElement("width")
            width_text = doc.createTextNode(str(v["width"]))
            width.appendChild(width_text)
            si.appendChild(width)

            height = doc.createElement("height")
            height_text = doc.createTextNode(str(v["height"]))
            height.appendChild(height_text)
            si.appendChild(height)

            deep = doc.createElement("depth")
            deep_text = doc.createTextNode(str(v["depth"]))
            deep.appendChild(deep_text)
            si.appendChild(deep)

        if k=="filename":
            fn = doc.createElement("filename")
            fn_text = doc.createTextNode(str(v))
            fn.appendChild(fn_text)
            annotationlist.appendChild(fn)

    with open(filename, "w") as f:
        f.write(doc.toprettyxml(indent="\t", encoding="utf-8"))

if __name__ == "__main__":
    print("It's a test!")
    mydict = {"object":{"bndbox":[[1,2,4,3], [2,3,4,5]],
                        "name":["chair", "horse"],
                        "difficult":[0,0]
                        },
              "size":{"width":500,
                      "height":375,
                      "depth":3},
              "owner":{"flickrid":"None",
                       "name":"?"},
              "source":{"database":"None",
                        "annotation":"like_voc_2007"},
              "filename":"00005.jpg"
              }
    pprint(mydict)
    write_dict_to_xml(mydict, "./001.xml")