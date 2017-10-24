# -*- encoding=utf-8
import os
import cv2
import tkFileDialog
import numpy as np

g_bDrawingBox = False # 用来判断鼠标是否在按下时移动，从判断是否需要绘制矩形框
g_mouse_event = False
option = None  # 标记退出选项
my_dict = {}  # 用于先存储数据
temp_dict = {}
box = [0, 0, 0, 0]
image = None  # 用于回调的图像


def on_mouse_handle(event, x, y, flags, l_image):
    global g_bDrawingBox
    global g_mouse_event
    global box
    global image

    if event == cv2.EVENT_LBUTTONDOWN:
        g_mouse_event = True  # 标记刚画完一个边框

        box[0] = x
        box[1] = y

        g_bDrawingBox = True
        #print("down:{},{}".format(box[0], box[1]))

    if event == cv2.EVENT_MOUSEMOVE:
        if g_bDrawingBox:
            # 用于显示绘图过程
            temp_image = image.copy()
            cv2.rectangle(temp_image, (box[0], box[1]), (x, y), (0, 0, 255), 2)
            cv2.imshow("image", temp_image)

    if event == cv2.EVENT_LBUTTONUP:
        g_bDrawingBox = False
        box[2] = x
        box[3] = y

        if box[0] < box[2] and box[1] > box[3]:
            box[1], box[3] = box[3], box[1]
        if box[0] > box[2] and box[1] < box[3]:
            box[0], box[2] = box[2], box[0]
        if box[0] > box[2] and box[1] > box[3]:
            box[0], box[2] = box[2], box[0]
            box[1], box[3] = box[3], box[1]

        if box[0] == box[2] or box[1] == box[3]:
            g_mouse_event = False
            return
        if (box[2]-box[0]) < 5 or (box[3]-box[1]) < 5:
            g_mouse_event = False
            return


        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        #print("up:{},{}".format(box[2], box[3]))
        cv2.imshow("image", image)


if __name__ == "__main__":
    # 选择要标注的图像路径
    image_path = tkFileDialog.askdirectory()
    try:
        image_path.split("/")[-1].split("_")[-1] == "pills"
    except:
        raise

    print(image_path)

    output_file = os.path.join(image_path, "output.txt")
    assert not os.path.exists(output_file), "请处理下output.txt,存在它说明你还没有进行Annotation！"
    list_files = os.listdir(image_path)

    # 显示图像，并标注
    image = None
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)  # 按图像大小自动显示
    cv2.moveWindow("image", 100, 100)  # 窗口显示在屏幕固定区域，方便标注
    cv2.setMouseCallback("image", on_mouse_handle, image) # 设置鼠标回调函数

    # 给图像标注有以下选项:1 n:下一张, ESC:退出, r:重绘
    # 这一步保证了图像是从000001索引按顺序开始进行标注的
    temp_list_files = []
    for i in range(len(list_files)):
        temp_list_files.append("{:06d}.jpg".format(i+1))
    list_files = temp_list_files[:]
    print(list_files)

    for i in range(len(list_files)):
        im_file = os.path.join(image_path, list_files[i])
        im = cv2.imread(im_file)

        image = im.copy()  # 复制一份图像
        cv2.imshow("image", image)

        while True:
            #该循环主要为标注矩形框负责，当绘制矩形框功能重置为False时，break
            if g_mouse_event == False: # 没开始画矩形框,或画完已正常处理了
                key = cv2.waitKey(1)
                if key == 27:
                    option = "ESC"
                    if temp_dict == {}:
                        break
                    else:
                        my_dict[list_files[i]] = temp_dict[list_files[i]]
                        temp_dict = {}
                        break  # 跳出while
                if key == ord("n"):
                    if temp_dict == {}:
                        option = "ESC"
                        break
                    else:
                        my_dict[list_files[i]] = temp_dict[list_files[i]]
                        temp_dict = {}
                        break  # 跳出while
                if key == ord("r"):
                    temp_dict = {}
                    image = im.copy()  # 复制一份图像
                    cv2.imshow("image", image)
                    continue

            else: # 刚刚画完边框
                key = cv2.waitKey(0) # 画完边框则无限期等待处理，输入键值

                if key == ord("n"):
                    print("else  n")
                    # 存入信息到my_dict
                    if temp_dict == {}:
                        option = "ESC" # 需要跳出for
                        break
                    else:
                        my_dict[list_files[i]] = temp_dict[list_files[i]]
                        temp_dict = {}
                        break  # 跳出while


                if key == ord("r"):
                    temp_dict = {}
                    image = im.copy()  # 复制一份图像
                    g_mouse_event = False
                    print("else  r")
                    cv2.imshow("image", image)
                    continue

                if key == 27:
                    print("else  Esc")
                    if temp_dict == {}:
                        option = "ESC" # 需要跳出for
                        break
                    else:
                        my_dict[list_files[i]] = temp_dict[list_files[i]]
                        temp_dict = {}
                        option = "ESC"
                        break # 跳出while

                # 输入有效键值了，存入信息到temp_dict
                if temp_dict == {}:
                    temp_dict[list_files[i]] = [[chr(key), box[0], box[1], box[2], box[3]]]
                else:
                    temp_dict[list_files[i]].append([chr(key), box[0], box[1], box[2], box[3]])
                #print(key)
                # 打印当前图像名，边框名，边框
                print("{}  {}  [{:3d}, {:3d}, {:3d}, {:3d}]".format(list_files[i], chr(key), box[0], box[1], box[2], box[3]))

                g_mouse_event = False

            cv2.imshow("image", image)

        if option == "ESC":
            break


    with open(output_file, "w") as f:
        # 将my_dict中的数据写入到output.txt中
        for k, v in my_dict.items():
            for l in range(len(v)):
                temp = "{} {} {} {} {} {}\n".format(k, v[l][0], v[l][1], v[l][2], v[l][3], v[l][4])
                f.write(temp)

    if my_dict == {}:
        os.remove(output_file)

