import os.path
from tqdm import tqdm

from moviepy.editor import VideoFileClip
from PIL import Image


def generate_cuts(video_path, save_path, fps):
    video = VideoFileClip(video_path)
    contrl_fps = int(video.fps/fps)
    assert isinstance(contrl_fps, int)

    for i, cut in tqdm(enumerate(video.iter_frames()), total=video.duration*video.fps):
        # 控制每秒的帧率
        if i%contrl_fps != 0:
            continue
        # 将帧转换为PIL图像
        img = Image.fromarray(cut)
        img.save(os.path.join(save_path, f"{int(i/contrl_fps):05d}.png"))


if __name__=='__main__':
    fps = 10
    generate_cuts("D:/Util/y2mate.com - Furina sing La vaguelette MMD Genshin_1080p.mp4","avater", fps)