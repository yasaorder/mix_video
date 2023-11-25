# mix_video
把芙芙的角色pv、剧情视频拼成轻链剧情pv

- 23/11/24 更新 增加了用moviepy分割视频每一帧的方法，可以不用安装ffmepg
- 23/11/25 增加了做屏风特效的代码：duominuo里的pingfeng函数

## 使用方法
用generate_cuts将视频按帧分割成图片，保存到图片集avater中，用generate根据目标视频的每一帧生成对应混合图片，
最后将这些混合后的图片导入剪映中，添加音频导出即可

### 效果演示：
【把芙芙的角色pv、剧情视频拼成轻涟剧情pv】 https://www.bilibili.com/video/BV1eH4y1q78z/?share_source=copy_web&vd_source=2e750978c40c2df84c94c73e870d8386

【用python做一张喜欢的壁纸的屏风特效】 https://www.bilibili.com/video/BV1vw411n7fK/?share_source=copy_web&vd_source=2e750978c40c2df84c94c73e870d8386

### generate_cuts
代替 cut.py ，将视频按帧分割成图片，保存到图片集avater中

### cut.py
将视频按帧分割成图片，保存到图片集avater中

### generate.py
根据目标视频的每一帧生成对应混合图片

### duominuo.py
做多米诺和屏风特效的代码，目前只完成了屏风

### generate_video.py
由生成的混合图片集生成视频。但是设备性能不行，或者代码没写好，没弄完。
这一步实际是由剪映完成的。

### generate_gpu.py
尝试用gpu加速计算没有完成

### video_add_audio.py
为视频添加音频文件


