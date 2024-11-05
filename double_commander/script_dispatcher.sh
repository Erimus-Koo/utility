#!/bin/bash
# 主要用于 Double Commander 的按钮
# 它只能调用一个外部可执行文件，不能直接调用 Python 或者其他程序，所以用一个代理来实现
# ⚠️ 结果发现可以把 Python 作为可执行文件，把 .py 作为参数传入。

# 获取所有传递的参数
params="$@"

# 设置常用变量
PYTHON_EXEC="/Users/erimus/.pyenv/shims/python"
DIR_SHARE="/Users/erimus/OneDrive/05ProgramProject/Python/utilities/share"

# 使用 osascript 弹出对话框显示参数
show_dialog() {
  local message="$@"
  osascript <<EOF
tell application "System Events"
    activate
    display dialog "$message"
end tell
EOF
}
# show_dialog "Received arguments:" $params

case "$1" in
  archive_file)
    $PYTHON_EXEC "$DIR_SHARE/archive_files.py" "${@:2}"
    ;;
  another_command)
    $PYTHON_EXEC "$DIR_SHARE/another_command.py" "${@:2}"
    ;;
  *)
    show_dialog "Unknown command: $1"
    ;;
esac
