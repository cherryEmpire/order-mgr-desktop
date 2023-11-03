# PYQT 一个小客户端

# 依赖
```commandline
pip3 install PySide6
pip3 install pinyin
```

# 打包
```text
pyinstaller -F -w main.py
pyinstaller -F -w --icon=main.ico main.py
```
# qrc
```text
pyside2-rcc xxxxx\ordermgr.qrc -o xxxxx\ordermgr.py
```