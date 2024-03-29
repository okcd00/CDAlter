# CDMouth
Mainly for TTS applications.


# Project Tree and Requirements

> 处理、播放 `.wav` 音频文件
+ [pydub](https://github.com/jiaaro/pydub)
    + `pydub>=0.24.1` 
+ [pyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
    + `pyaudio>=0.2.11` 
+ [ffmpeg](https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200309-608b8a8-win64-static.zip)
  + [win32/static](https://ffmpeg.zeranoe.com/builds/win32/static/)
  + [win64/static](https://ffmpeg.zeranoe.com/builds/win64/static/)
  + [macos/static](https://ffmpeg.zeranoe.com/builds/macos64/static/)


# TroubleShooter

> FileNotFoundError: [WinError 2] 系统找不到指定的文件

in subprocess.py, find class Popen, set `shell = True` in `__init__()`

> Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work

in utils.py, add this in `which()`:
```
envdir_list.append('E:\\ffmpeg\\ffmpeg-20200309-608b8a8-win64-static\\bin')
```

> I want to transfer `.mp3` to `.wav`

```shell
# 转换amr到mp3：
ffmpeg -i shenhuxi.amr amr2mp3.mp3
# 转换amr到wav：
ffmpeg -acodec libamr_nb -i shenhuxi.amr amr2wav.wav
# 转换mp3到wav：
ffmpeg -i DING.mp3 -f wav test.wav
# 转换wav到amr：
ffmpeg -i test.wav -acodec libamr_nb -ab 12.2k -ar 8000 -ac 1 wav2amr.amr
# 转换wav到mp3：
ffmpeg -i test.wav -f mp3 -acodec libmp3lame -y wav2mp3.mp3

# 转换wmv到mp4：
ffmpeg -i sample.wmv -vcodec libx264 -acodec aac out.mp4
# 将H264视频流转为mp4:
ffmpeg -i sample.h264 -f mp4 haha.mp4
```