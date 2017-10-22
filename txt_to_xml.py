# -*- encoding=utf-8
import os
import Tkinter
import tkFileDialog
import cv2
import pprint
from dict_to_xml import write_dict_to_xml

def txt_to_xml(filename, target):
    target.delete(0.0, Tkinter.END)
    txt_dir = filename.get()
    if not os.path.exists(txt_dir):
        target.insert(0.0, "路径目录不存在:" + txt_dir)
        return

    xml_dir = os.path.join(txt_dir, "xml")
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    target.insert(0.0, "正在转化...")
    #*****************************************************************************
    #此处根据情况修改txt到xml转化具体实现（取决于两者对接）
    all_dict = {}
    with open(txt_dir+"/output.txt", "r") as f_txt:
        file_dict = {}
        for line in f_txt.readlines():
            filename, checkwell, xmin, ymin, xmax, ymax = line.split()

            im_path = os.path.join(txt_dir, filename)
            #print(im_path)
            im = cv2.imread(im_path)
            im_height, im_width, im_depth = im.shape
            #print(im.shape, checkwell, xmin, ymin, xmax, ymax)

            temp_dict = {}
            temp_dict["filename"] = filename
            temp_dict["size"] = {}
            temp_dict["size"]["width"] = im_width
            temp_dict["size"]["height"] = im_height
            temp_dict["size"]["depth"] = im_depth
            temp_dict["object"] = {}
            temp_dict["object"]["bndbox"] = [[xmin, ymin, xmax, ymax]]
            temp_dict["object"]["name"] = ["white_" + checkwell]
            temp_dict["object"]["difficult"] = [0]
            if not all_dict.has_key(filename):
                # 新建
                all_dict[filename] = temp_dict
                #print(temp_dict)
            else:
                #添加
                all_dict[filename]["object"]["bndbox"].append(temp_dict["object"]["bndbox"][0])
                all_dict[filename]["object"]["name"].append(temp_dict["object"]["name"][0])
                all_dict[filename]["object"]["difficult"].append(temp_dict["object"]["difficult"][0])

    print(all_dict)
    for k, v in all_dict.items():
        filenamepath = os.path.join(xml_dir, k.split(".")[0]+".xml")
        write_dict_to_xml(v, filenamepath)
    #**************************************************************************
    target.insert(1.0, "转化完成！")


def xml_to_txt(filename, target):
    print(filename.get())


def check_dir(write_to, target):
    f = tkFileDialog.askdirectory()

    # 清空数据
    write_to.delete(0, Tkinter.END)
    target.delete(0.0, Tkinter.END)

    # 显示数据
    write_to.insert(0, f)
    target.insert(0.0, "readed dir: " + write_to.get())



if __name__ == "__main__":
    top = Tkinter.Tk()
    top.geometry("500x300")
    top.title("txt与xml转化demo")

    frame2 = Tkinter.Frame(top)
    multi_text = Tkinter.Text(frame2)
    multi_text.pack()
    frame2.grid(row=1, column=0)


    frame1 = Tkinter.Frame(top)

    frame_title1 = Tkinter.Frame(frame1)
    Tkinter.Label(frame_title1, text="txt所在目录").grid()
    Tkinter.Label(frame_title1, text="xml所在目录").grid()
    entry1 = Tkinter.Entry(frame_title1)
    entry2 = Tkinter.Entry(frame_title1)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    frame_title1.grid(row=0, column=0, sticky=Tkinter.E)

    frame_title2 = Tkinter.Frame(frame1)
    button_check1 = Tkinter.Button(frame_title2, text="浏览", command=lambda x=entry1, y=multi_text:check_dir(write_to=x, target=y))
    button_check2 = Tkinter.Button(frame_title2, text="浏览", command=lambda x=entry2, y=multi_text:check_dir(write_to=x, target=y))
    button_check1.grid(row=0, column=0)
    button_check2.grid(row=1, column=0)
    frame_title2.grid(row=0, column=1)

    frame_title3 = Tkinter.Frame(frame1)
    button_t_x = Tkinter.Button(frame_title3, text="txt to xml", command=lambda x=entry1, y=multi_text: txt_to_xml(filename=x, target=y))
    button_x_t = Tkinter.Button(frame_title3, text="xml to txt", command=lambda x=entry2, y=multi_text: xml_to_txt(filename=x, target=y))
    button_t_x.grid(row=0, column=0)
    button_x_t.grid(row=1, column=0)
    frame_title3.grid(row=0, column=2, sticky=Tkinter.W)

    frame1.grid(row=0, column=0)

    Tkinter.mainloop()