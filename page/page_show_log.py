from PyQt5.QtWidgets import  QLabel
from PyQt5.QtCore import Qt, QTimer

import setting


class ShowLog(QLabel):
    def __init__(self, text,time_end=2000,color=(255,255,0)):
        super().__init__()
        # 关键设置顺序不可调换
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 第一顺位
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景支持
        self.setObjectName("frame_bubble")
        self.setStyleSheet(f"""#frame_bubble
                            {{
                                background: rgba(17, 24, 30, 255);
                           
                                padding: 20px;
                                border: 3px solid rgb(103, 82, 44);
                                color: rgb{color}; /* 仅设置文字颜色 */
                                font-size: {setting.font.pointSize()+5}pt;
                            }}""")
        self.setWindowOpacity(0.8)#设置1-0之间设置窗口透明度
        #左右中间对齐
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.adjustSize()
        # 设置2秒后自动关闭
        QTimer.singleShot(time_end, self.close)

if __name__ == '__main__':
    show_log = ShowLog("这是一个穿透鼠标的气泡提示\n支持多行文本")
    show_log.show()

