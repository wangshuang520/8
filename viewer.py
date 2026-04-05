import sys
import struct
import requests
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, 
                             QVBoxLayout, QWidget, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class SmartImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.update_url = None
        self.current_pixmap = None
        
        self.init_ui()
        self.load_and_check_image()
        
    def init_ui(self):
        self.setWindowTitle("智能聊天图片查看器")
        self.setGeometry(100, 100, 450, 800)
        
        # 布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 图片显示区域
        self.image_label = QLabel("正在加载...")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("检查远程更新")
        self.refresh_btn.clicked.connect(self.check_remote_update)
        layout.addWidget(self.refresh_btn)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def load_and_check_image(self):
        # 1. 先正常加载图片显示
        self.display_image(self.image_path)
        
        # 2. 尝试读取隐藏的更新地址
        try:
            with open(self.image_path, 'rb') as f:
                data = f.read()
            
            marker = b'__SMART_CHAT_UPDATE__'
            marker_pos = data.find(marker)
            
            if marker_pos != -1:
                # 找到了标记，读取URL
                url_start = marker_pos + len(marker)
                # 读取4字节长度
                url_len_data = data[url_start : url_start + 4]
                url_len = struct.unpack('>I', url_len_data)[0]
                # 读取URL
                url_bytes = data[url_start + 4 : url_start + 4 + url_len]
                self.update_url = url_bytes.decode('utf-8')
                self.status_label.setText(f"✅ 已绑定远程地址，正在自动检查...")
                
                # 延迟2秒自动检查一次更新
                QTimer.singleShot(2000, self.check_remote_update)
            else:
                self.status_label.setText("这是一张普通图片，无远程更新功能")
                
        except Exception as e:
            self.status_label.setText(f"读取出错: {str(e)}")

    def display_image(self, path_or_data):
        if isinstance(path_or_data, str):
            pixmap = QPixmap(path_or_data)
        else:
            image = QImage.fromData(path_or_data)
            pixmap = QPixmap.fromImage(image)
        
        # 缩放适应窗口
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.current_pixmap = pixmap

    def check_remote_update(self):
        if not self.update_url:
            QMessageBox.warning(self, "提示", "没有找到远程更新地址")
            return
        
        self.status_label.setText("🔄 正在连接远程服务器检查更新...")
        self.refresh_btn.setEnabled(False)
        
        try:
            # 发送请求获取图片
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                # 成功获取，显示新图片
                self.display_image(response.content)
                self.status_label.setText("🎉 已更新为最新远程图片！")
                QMessageBox.information(self, "成功", "图片已远程更新！")
            else:
                self.status_label.setText(f"检查失败，状态码: {response.status_code}")
        except Exception as e:
            self.status_label.setText(f"网络错误: {str(e)}")
        finally:
            self.refresh_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if len(sys.argv) > 1:
        # 如果是拖拽图片打开，或者右键选择打开方式
        img_path = sys.argv[1]
    else:
        # 默认尝试打开同目录下的 smart_chat.png
        img_path = "smart_chat.png"
    
    viewer = SmartImageViewer(img_path)
    viewer.show()
    sys.exit(app.exec_())
