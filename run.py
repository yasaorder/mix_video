import os
from PIL import Image
import matplotlib.pyplot as plt
import time
def show_images(directory):
    num = len(os.listdir(directory))
    for i in range(0, num, 3):
        filename = f'{i}.jpg'
        if filename.endswith(".jpg") or filename.endswith(".png"):  # 如果文件是图片
            img = Image.open(os.path.join(directory, filename))  # 打开图片
            img
            img.show()  # 展示图片
            time.sleep(1)  # 等待1秒，展示下一张图片

            img.close()

            """# 创建一个图像
            img = plt.imread(os.path.join(directory, filename))

            # 设置图像显示位置（x，y）和大小（width，height）
            x = 0
            y = 0
            width = 6400
            height = 3600

            # 在指定位置展示图像
            plt.imshow(img, extent=(x, x + width, y, y + height))
            # 开启交互模式，否则当运行到show时，代码会陷入停止
            plt.ion()
            plt.show()
            print(f"{i}")
            time.sleep(20)

            plt.close()"""


if __name__ == '__main__':
    show_images("gener")