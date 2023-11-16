import os
import uuid
# from ffmpy import FFmpeg


# 视频添加音频
# def video_add_audio(video_path: str, audio_path: str, output_dir: str):
#     _ext_video = os.path.basename(video_path).strip().split('.')[-1]
#     _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
#     if _ext_audio not in ['mp3', 'wav']:
#         raise Exception('audio format not support')
#     _codec = 'copy'
#     if _ext_audio == 'wav':
#         _codec = 'aac'
#     result = os.path.join(
#         output_dir, '{}.{}'.format(
#             uuid.uuid4(), _ext_video))
#     ff = FFmpeg(
#         inputs={video_path: None, audio_path: None},
#         outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -shortest'.format(_codec)})
#     print(ff.cmd)
#     ff.run()
#     return result

from moviepy.editor import *


def format_type(name):
    """
    判断 name 是视频格式还是音频格式
    """
    try:
        if name.endswith('.mp3') or name.endswith('.wav') or name.endswith('.flac'):
            return "audio"
        elif name.endswith('.mp4') or name.endswith('.avi') or name.endswith('.mov'):
            return "video"
        else:
            return "无法识别"
    except ValueError:
        print("未能识别的文件格式")


def add_audio(video_path:str, out_path:str, audio_path=None):
    """
    添加音频， 如果想要加入目标视频之外的视频，可以通过 audio_name 参数添加
    否则添加目标视频的视频
    """
    print("添加音频")
    video = VideoFileClip(video_path)
    if audio_path != None:
        if format_type(audio_path) == 'audio':
            audio = AudioFileClip(audio_path)
        elif format_type(audio_path) == 'video':
            video_add = VideoFileClip(audio_path)
            audio = video_add.audio
            audio = audio.subclip()
    elif audio_path == None:
        audio = video.audio
        audio = audio.subclip()

    audio.write_audiofile("qinglian.mp3")

    # 将音频添加到视频中
    # final_clip = video.set_audio(audio)

    # 导出结果
    # final_clip.write_videofile(out_path)


if __name__ == '__main__':
    add_audio("qinglian.mp4", "try_2.mp4", "qinglian.mp4")