from PIL import Image
import numpy as np
from pathlib import Path
from rich.progress import track
from scipy.spatial import KDTree
import os
import concurrent.futures
import imageio
from PIL import Image
from generate_video import generate_video
from video_add_audio import add_audio
from moviepy.editor import VideoFileClip

folder = Path('avater')

# 计算每张图片的颜色值，并存储在data.npy里
def calc_all_colors():
    res = []
    for file in track(list(folder.glob('*.png'))):
        img = Image.open(file)
        mat = np.asarray(img)
        color = np.mean(mat, (0, 1))
        res.append((file.name, color))

    np.save('data.npy', np.array(res, dtype=object))


# 根据原始图片集生成，和目标图片相似的一张混合的图片
def generate_img(save_img_path, target_img_path=None, target_img=None, type='img'):
    colors = np.load('data.npy', allow_pickle=True)
    files = colors[:, 0]
    rgbs = np.array([c[1] for c in colors])
    tree = KDTree(rgbs)
    #用KDT存储小图片，因为大量的图片按list遍历查询最接近的图片太复炸了
    #这是一种类似三维空间的遍历，节约查询颜色相似的图片的时间

    target = None
    if type == 'img':
        target = target_img
    elif type == 'path':
        target = Image.open(target_img_path)

    piece_width = 100
    resize_width = 100
    resize_height = int(target.height * resize_width / target.width)
    target = target.resize((resize_width, resize_height))
    mat = np.asarray(target)
    canvas = Image.new(
        'RGB', (resize_width * piece_width, resize_height * piece_width))
    # 画板，也就是合成图片
    for i in track(range(resize_height), total=resize_height):
        for j in range(resize_width):
            color = mat[i, j].astype(np.float32)
            dist, idx = tree.query(color, k=20)
            #查询小图片中最接近的k个
            # 因为只取一个，大图片中相似的位置都会用同一个图片合成
            # idx是colors的第0列
            ind = np.random.choice(idx)
            # 避免重复
            dist = dist[idx.tolist().index(ind)]
            # 记录所取图片的distance，如果太远，对原图片做一些修改
            imgfile = folder / files[ind]
            #所要的图片
            img = Image.open(imgfile)
            img = img.resize((piece_width, piece_width))
            if dist > 30:
                offset = color - rgbs[ind]
                m = np.asarray(img, dtype=np.float32)
                m += offset
                m.clip(0, 255, out=m)
                # 因为加上offst可能会超出0-255的范围
                # 如果没有clip会产生很严重的偏差，故要裁剪输出到out
                # 原来（-10，260）转uint8会是（246，4）
                # clip先转为（0，255），再转uint8
                img = Image.fromarray(m.astype(np.uint8))
                # 先转为uint8格式，uint8范围0-255，
                # 从而能正常地转化为图片
            canvas.paste(img, (j * piece_width, i * piece_width))
            #画到图片对应位置
    canvas.save(save_img_path)

def main():
    # 读取视频文件
    video = VideoFileClip("qinglian.mp4")

    video_imgs_path = "gener/"

    calc_all_colors()

    # 遍历视频的每一帧
    for i, frame in enumerate(video.iter_frames()):
        if i<=4569:
            continue
        if i%3 != 0:
            continue
        # 将帧转换为PIL图像
        img = Image.fromarray(frame)

        # 保存图像
        # img.save(f"gener/{i}.jpg")
        # 生成图像

        img_path = video_imgs_path+f"{i}.jpg"
        generate_img(img_path, None, img, 'img')
        print(f"{i}.jpg 已完成" )

    # 生成视频
    # generate_video(video_imgs_path, 'noaudio.mp4',30)

    # 添加音频
    # add_audio('noaudio.mp4', '', 'output.mp4')

    # 视频时长（秒）
    # duration = video.duration
    # print(f"Converted {duration} frames.")


if __name__ == '__main__':
    main()