# mkv格式的视频，其字幕是内嵌在图片中的
# 从而避免了截图时保留字幕
import os
# os.system("ffmpeg -i .\*.mkv -ss 0:1:0 -t 0:0:10 -vf fps=1 thumb%"
# 从0h1m开始间隔时间10s，设置videofitter，
# 一秒只有一帧，输出为thumb*.png

os.system('ffmpeg -i shuishenzhiwu.mp4 -vf "crop=x=0:y=0:w=1280:h=720,scale=640:-1,fps=2" avater/shuishenzhiwu%04d.png')
os.system('ffmpeg -i fufupv.mp4 -vf "crop=x=0:y=0:w=1280:h=720,scale=640:-1,fps=2" avater/fufupv%04d.png')
os.system('ffmpeg -i fufuyanshi.mp4 -vf "crop=x=0:y=0:w=1280:h=720,scale=640:-1,fps=2" avater/fufuyanshi%04d.png')
#只需要裁剪一段视频中的区域
#crop代表一个矩形框，xy为左上角的坐标
#scale用来缩放图片，-1意味着根据前面的宽度等比例缩放
#fps代表每秒的取样次数，如fps=1，每秒截取一张图片
# 因为输出有1万张，所以05d的格式比较合适