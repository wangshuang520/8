@echo off
echo 正在打包查看器为 EXE 文件...
pyinstaller --onefile --windowed --name "智能图片查看器" viewer.py
echo.
echo ✅ 打包完成！
echo 可执行文件在 dist 文件夹里：智能图片查看器.exe
pause
