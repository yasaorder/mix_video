# import os
# import cv2
# import time
import math

# img_root = "../img/"
# path="../img/"
# filelist=os.listdir()
# fps = 2
# # file_path='saveVideo.avi' # 导出路径MJPG
# # file_path='saveVideo'+str(int(time.time()))+'.mp4' # 导出路径DIVX/mp4v
# file_path='saveVideo.mp4' # 导出路径DIVX/mp4v
# size=(3968,2976)
#
# #可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
# # fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # avi
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4
#
# videoWriter = cv2.VideoWriter(file_path,fourcc,fps,size)
#
# # 这种情况更适合于照片是从"1.jpg" 开始，然后每张图片名字＋1的那种
# # for i in range(8):
# #     frame = cv2.imread(img_root+str(i+1)+'.jpg')
# #     videoWriter.write(frame)
#
# for item in filelist:
#     if item.endswith('.jpg'):   #判断图片后缀是否是.jpg
#         item = path  + item
#         img = cv2.imread(item) #使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
#         # print(type(img))  # numpy.ndarray类型
#         videoWriter.write(img)        #把图片写进视频
#
#
#
# videoWriter.release() #释放

import numpy as np
import os
import concurrent.futures
import imageio
from PIL import Image


def generate_video(in_files_path:str, save_video_path:str, fps=30):
    # 设置生成的视频文件名和路径
    # filepath = os.path.join(os.getcwd(), filename)
    # os.getcwd()代表生成在当前目录下
    print("生成视频文件")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 寻找所有 图片 文件
        # image_files = [os.path.join(in_files_path, file) for file in os.listdir(in_files_path) if file.endswith(".png")]
        image_files = [os.path.join(in_files_path, file) for file in os.listdir(in_files_path) if file.endswith(".jpg")]

        # 利用线程池并行处理图像
        # 由于图片空间太大需要分组
        # img_len = len(image_files)
        # group_num = math.floor(img_len/100) + 1
        # images = []
        # for i in range(group_num):
        #     images.append = list(executor.map(process_image, image_files[i*100: i+1*100]))
        images = list(executor.map(process_image, image_files[0: 100]))

    # 将图片转换为视频文件
    with imageio.get_writer(save_video_path, fps=fps) as video:
        # for i in range(group_num):
        for i, image in enumerate(images):
            video.append_data(image)
            print(f"{i} added")

    video.close()


def process_image(file_path):
    image = Image.open(file_path)
    if file_path.endswith(".png"):
        image = image.convert("RGB")

    return np.asarray(image)


if __name__ == '__main__':
    i = [1,2,3]

    generate_video("gener/", "try_1.mp4", 10)