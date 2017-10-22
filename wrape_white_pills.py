# -*- encoding=utf-8
import os 
import cv2


def _get_write_from_path():
	cur_dir = os.path.dirname(__file__)
	wp_path = os.path.join(cur_dir, "data", "origin_data", "white_pills")
	assert os.path.exists(wp_path), "{} not exists".format(wp_path)
	return wp_path

def _get_write_to_path():
	cur_dir = os.path.dirname(__file__)
	wt_path = os.path.join(cur_dir, "data", "white_pills")
	assert os.path.exists(wt_path), "{} not exists".format(wt_path)
	return wt_path

def wrape_white_pills():
	write_to_path = _get_write_to_path()
	write_from_path = _get_write_from_path()
	# 先判断是否完成标注转化，即有无ouput.txt文件
	output = os.path.join(write_to_path, "output.txt")
	if os.path.exists(output):
		print("{}存在，请先完成相应标注转化！".format(output))
		return

	list_to_images = os.listdir(write_to_path)
	list_from_images = os.listdir(write_from_path)
	# 转化相应.bmp文件为.jpg
	print("此次从{}添加图像数量:{}".format(write_from_path, len(list_from_images)))
	for i in range(len(list_from_images)):
		# 读取源文件
		origin_image_ext = os.path.join(write_from_path, list_from_images[i])
		origin_image = cv2.imread(origin_image_ext)
		# 写入目标文件
		target_image_ext = os.path.join(write_to_path, "{:06d}.jpg")
		target_image = origin_image[500:, 50:-50, 0:3]  # 此处可以修改
		cv2.imwrite(target_image_ext.format(len(list_to_images) + i + 1), target_image)
		# 删除源文件
		os.remove(origin_image_ext)

	print("从{}转化完成！".format(write_from_path))

if __name__ == "__main__":
	pass
		


