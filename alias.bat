@echo off
doskey youget = python %~dp0youget.py $*
doskey submerge = python %~dp0image_tools\sub_merge.py $*
doskey resave = python %~dp0image_tools\image_save_as.py $*
doskey saveas = python %~dp0image_tools\image_save_as.py $*
doskey subfont = python %~dp0subtitle\format_sub_font.py $*
doskey remotekey = python %~dp0remote_key_service.py $*
doskey sidebar = python %~dp0generate_docsify_sidebar.py $*
