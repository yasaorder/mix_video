from PIL import Image
import numpy as np
from tqdm import tqdm
import os
import math
import concurrent.futures
import imageio
import cv2
from PIL import Image, ImageOps
from moviepy.editor import VideoFileClip

# 计算每张图片的颜色值，并存储在data.npy里
def generate_one_row(map, start_pixel, end_pixel, fps):
    """
    生成一列的多米诺牌的动画
    """
    canvas = map.copy()

    # 获取图像shape
    height = map.shape[0]
    cut = (start_pixel - end_pixel) / fps

    cropped = canvas[0:height, end_pixel:start_pixel]
    row_list = []

    for i in range(1, fps-2):
        # 设置图像仿射变化矩阵
        # 因为是对cropped 做仿射变换，所以坐标也是cropped的坐标
        post_pre = np.float32([[0, 0], [0, height], [start_pixel-end_pixel, height], [start_pixel-end_pixel, 0]])
        new_pixel = start_pixel - end_pixel - i * cut
        post_aft = np.float32([[0, 0], [0, height], [new_pixel, height], [new_pixel, 0]])
        M = cv2.getPerspectiveTransform(post_pre, post_aft)
        # 图像变换
        result = cv2.warpPerspective(cropped, M, (start_pixel - end_pixel, height))
        mask = np.ones_like(cropped)*255
        mask[:,0:int(new_pixel),:] = result[:,0:int(new_pixel),:]
        # cv2.imshow("s",mask)
        # cv2.waitKey(0)

        canvas[0:height, end_pixel:start_pixel, :] = mask[:, :, :]
        # cv2.imshow("c", canvas)
        # cv2.waitKey(0)
        frame_canvas = cv2.cvtColor(canvas.copy(), cv2.COLOR_BGR2RGB)
        row_list.append(frame_canvas)

    return canvas, row_list, end_pixel


def generate_all_row(map, all_start_pixel, all_end_pixel, bound_w, fps):
    """
    生成多列的多米诺牌的动画
    """
    # 获取图像shape
    height = map.shape[0]
    # 每帧移动的像素
    cut = bound_w / fps
    # 将图片分为的格数
    gaps_num = (all_start_pixel-all_end_pixel) // bound_w
    # 存储的列表
    rows = []
    # 新建画布
    # 因为这个画布是要一直用的，所以放在外面
    canvas = map.copy()

    for f_i in range(0, fps-1):

        for gap_i in range(gaps_num):
            # 遍历每个需要变换的位置
            start_pixel = all_start_pixel - gap_i * bound_w
            end_pixel = start_pixel - bound_w
            cropped = canvas[0:height, end_pixel:start_pixel]
            # cv2.imshow("s",cropped)
            # cv2.waitKey(0)

            # 设置图像仿射变化矩阵
            # 因为是对cropped 做仿射变换，所以坐标也是cropped的坐标
            post_pre = np.float32([[0, 0], [0, height], [start_pixel-end_pixel, height], [start_pixel-end_pixel, 0]])
            new_pixel = start_pixel - end_pixel - f_i * cut
            post_aft = np.float32([[0, 0], [0, height], [new_pixel, height], [new_pixel, 0]])
            M = cv2.getPerspectiveTransform(post_pre, post_aft)
            # 图像变换
            result = cv2.warpPerspective(cropped, M, (start_pixel - end_pixel, height))
            mask = np.ones_like(cropped)*255
            mask[:,0:int(new_pixel),:] = result[:,0:int(new_pixel),:]
            # cv2.imshow("s",mask)
            # cv2.waitKey(0)

            canvas[0:height, end_pixel:start_pixel, :] = mask[:, :, :]

        # cv2.imshow("c", canvas)
        # cv2.waitKey(0)
        # 格式转换, 否则图片颜色会偏红
        frame_canvas = cv2.cvtColor(canvas.copy(),cv2.COLOR_BGR2RGB)
        rows.append(frame_canvas)

    for i in range(10):
        frame_canvas = cv2.cvtColor(canvas.copy(), cv2.COLOR_BGR2RGB)
        rows.append(frame_canvas)

    return rows


def preprocess(img, bound_w, bound_h, fps):
    """
    resize 图像， 不足以白色填充
    """
    img_w, img_h = img.size  # 原始图像的尺寸
    temp1 = lcm(bound_w, 16, fps) # 保证能被16和牌的宽度整除
    temp2 = lcm(bound_h, 16, fps)
    final_width = img_w // temp1 * temp1
    if final_width < img_w:
        final_width = final_width + temp1
    final_height = img_h // temp2 * temp2# 目标图像的尺寸
    if final_height < img_h:
        final_height = final_height + temp2

    print("original size: ", (img_w, img_h))
    print("new size: ", (final_width, final_height))

    scale = min(final_width / img_w, final_height / img_h)  # 转换的最小比例

    # 保证原图的长或宽，至少一个符合目标图像的尺寸 0.5保证四舍五入
    new_img_w = int(img_w * scale + 0.5)
    new_img_h = int(img_h * scale + 0.5)

    img_resized = img.resize((new_img_w, new_img_h), Image.LANCZOS)

    final_image = Image.new('RGB', (final_width, final_height), (255, 255, 255))  # 生成白色图像
    # // 为整数除法，计算图像的位置
    final_image.paste(img_resized, ((final_width - new_img_w) // 2, (final_height - new_img_h) // 2))  # 将图像填充为中间图像，两侧为黑色的样式
    final_image = np.asarray(final_image)
    final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite('resize.png', final_image)

    return final_width, final_height, final_image

def lcm(x:int, y:int, z:int):
    """
    求最小公倍数
    """
    gcd1 = math.gcd(x, y)
    lcm1 = x * y // gcd1
    gcd2 = math.gcd(lcm1, z)
    lcm2 = lcm1 * z // gcd2
    return lcm2


def pingfeng(target_path, save_video_path, fps, duration):
    """
    输出屏风风格的视频
    """
    # 读取图片
    target_img = Image.open(target_path)
    # 牌的大小
    bound_w, bound_h = 160, 80
    resize_bound_w, resize_bound_h = bound_w, bound_h
    # 调整图片形状
    resize_img_w, resize_img_h, orig_map = preprocess(target_img, resize_bound_w, resize_bound_h,fps)

    newmap = orig_map.copy()
    start_pixel = resize_img_w
    # 这里的 fps 让视频长一些，视频长度与这里的 fps 成正比
    rows = generate_all_row(newmap, start_pixel, 0, resize_bound_w, fps * duration)

    # 制作视频
    # i = 0
    # for image in tqdm(rows[::-1], total=len(rows)):
    #     # cv2.imwrite(save_video_path + f'{i}.png', image)
    #     img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #     img.save(save_video_path + f'{i}.png')
    #     i = i + 1
    #     # video.append_data(image)
    #
    # # orig_map = cv2.cvtColor(orig_map, cv2.COLOR_BGR2RGB)
    # for i in range(fps):
    #     img = Image.fromarray(cv2.cvtColor(orig_map, cv2.COLOR_BGR2RGB))
    #     img.save(save_video_path + f'{i}.png')
    #     # cv2.imwrite(save_video_path + f'{i}.png', orig_map)
    #     i = i + 1

    with imageio.get_writer(save_video_path, fps=fps) as video:
        for image in tqdm(rows[::-1], total=len(rows)):
            img = cv2.resize(image,[1936,1088])
            video.append_data(img)

        # orig_map = cv2.cvtColor(orig_map, cv2.COLOR_BGR2RGB)
        # for i in range(fps//10):
        #     o_img = cv2.resize(orig_map, [1936, 1088])
        #     video.append_data(o_img)

    video.close()


def duominuo(target_path, save_video_path, fps, times=2):
    # 读取图片
    target_img = Image.open(target_path)
    # 牌的大小
    bound_w, bound_h = 10, 8
    resize_bound_w, resize_bound_h = bound_w, bound_h
    # 调整图片形状
    resize_img_w, resize_img_h, orig_map = preprocess(target_img, resize_bound_w, resize_bound_h,fps)
    # 牌的列数
    # 从左到右倒
    row_num = resize_img_w // resize_bound_w

    newmap = orig_map.copy()
    rows_list = []
    start_pixel = resize_img_w
    for i in range(row_num):
        # 画出每一行的动画
        end_pixel = start_pixel - resize_bound_w
        newmap, row ,temp_pixel= generate_one_row(newmap, start_pixel, end_pixel, fps*times)
        start_pixel = temp_pixel
        row_copy = row.copy()
        rows_list.append(row_copy)

    # 制作视频
    with imageio.get_writer(save_video_path, fps=fps) as video:
        for row in tqdm(rows_list[::-1], total=len(rows_list)):
            for image in tqdm(row[::-1], total=len(row)):
                video.append_data(image)

        orig_map = cv2.cvtColor(orig_map, cv2.COLOR_BGR2RGB)
        for i in range(fps):
            video.append_data(orig_map)

    video.close()


if __name__ == '__main__':
    target_path = "sikeke.png"
    save_duominuo_path = 'duominnuo.mp4'
    save_pingfeng_path = 'pingfeng.mp4'
    # duominuo(target_path, save_duominuo_path, fps=60, times=1)

    # pingfeng("fufu/5_clear.png", 'video/1.mp4', fps=20, duration=10)
    pingfeng("fufu/7_clear.png", 'video/2.mp4', fps=20, duration=10)
    pingfeng("fufu/10_clear.png", 'video/3.mp4', fps=20, duration=10)
    pingfeng("fufu/24_clear.png", 'video/4.mp4', fps=20, duration=10)
    pingfeng("fufu/25_clear.png", 'video/5.mp4', fps=20, duration=10)
    pingfeng("fufu/27_clear.png", 'video/6.mp4', fps=20, duration=10)
