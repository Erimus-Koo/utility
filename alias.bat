@echo off

set private=D:\OneDrive\05ProgramProject\Python\utilities\private\
rem echo %private%

rem 开机自运行服务
doskey autorun = python %~dp0autorun.py $*

rem you-get 自动走代理且以最小画素下载
doskey youget = python %~dp0youget.py $*

rem 合并当前目录下的下载的音视频片段（youtube下载的分离文件）
doskey mergevideo = python %~dp0merge_video.py $*

rem 视频剪辑及合并
doskey trimvideo = python %~dp0trim_video.py $*

rem ffmpeg 格式转化
doskey videocvt = python %~dp0ffmpeg_format_converter.py $*

rem ffmpeg 音画不同步
doskey sounddelay = python %~dp0sound_delay.py $*

rem 影视台词拼图
doskey submerge = python %~dp0image_tools\sub_merge.py $*

rem ass字幕 默认字体改雅黑
doskey subfont = python %~dp0subtitle\format_sub_font.py $*

rem 图片另存 去隐私
doskey resave = python %~dp0image_tools\image_save_as.py $*
doskey saveas = python %~dp0image_tools\image_save_as.py $*

rem 检查当前目录的重复图片
doskey sameimg = python %~dp0image_tools\image_duplicated_lite.py $*

rem 启动本机rest api
doskey remotekey = python %~dp0remote_key_service.py $*

rem docsify生成侧边栏
doskey sidebar = python %~dp0generate_docsify_sidebar.py $*

rem 同步到我的cos 可以跟一个目录名参数
doskey sync = python %private%qcloud\erimuscc.py $*

rem 自动格式化文件 主要是markdown
doskey fmt = python %~dp0auto_format.py $*

rem 自动整理电脑上的琐碎文件
doskey clean = python %~dp0organize_personal_files.py $*

rem 表情包整理 自动从webp转png
doskey sticker = python D:\References\sticker\sticker.py $*

rem m3u8下载器
doskey m3u8 = python %private%m3u8.py $*

rem 定期起身运动
doskey gym = python %~dp0gym_timer.py $*

rem 终止进程
doskey kill = python %~dp0kill_process.py $*

rem 保持亮屏
doskey wake = python %~dp0windows_keep_awake.py $*

rem 网易云音乐 ncm 批量转mp3
doskey ncm = python %~dp0ncm_dump_batch.py $*

rem 重启icloud drive
doskey icloud = python %~dp0icloud_restart.py $*
