rem delete old files
del core.html
del core.c
rd /s /q build
del core.cp37-win_amd64.pyd

rem compiling
"C:\Program Project\Python 3.7.7\python.exe" setup.py build_ext --inplace

rem delete unnecessary files after compilation
del core.html
del core.c
rd /s /q build

rem move the core to the blender addon folder
move core.cp37-win_amd64.pyd ..\molecular\core.cp37-win_amd64.pyd

pause
