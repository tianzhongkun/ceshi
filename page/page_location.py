from PyQt5 import QtCore
from PyQt5.Qt import *

import setting
from setting import ratio, Path_img, Path_chess
from tft import tft
from tools.utils import clear_layout, chessId_get_data
from ui.form_location import Ui_FormLocation
from page.page_item_hexagon_label import HexagonLabel
class FormLocation(QWidget, Ui_FormLocation):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.frame.setObjectName("frame_box")
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 第一顺位
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景支持
        self.setVisible(True)
        #self.frame.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景支持
        self.setWindowOpacity(0.7)  # 设置1-0之间设置窗口透明度
        self.h_box_list = []  # 横向的
    def set_ui(self):
        pass
    def set_location(self,strategy=None):

        if strategy is None:
            return
        if setting.mode == 1:
            chess_list = tft.chess_list
        else:
            chess_list = tft.chess_list2
        # 清空box
        clear_layout(self.v_box)
        hero_location = strategy['detail']['hero_location']

        self.h_box_list = []  # 横向的
        for i in range(4):
            h_box = QHBoxLayout()
            h_box.setContentsMargins(0, 0, 0, 0)
            h_box.setSpacing(int(12*ratio))

            self.h_box_list.append(h_box)

            if i==1 or i==3:
                spacerItem = QSpacerItem(int(40*ratio), int(10*ratio))
                h_box.addItem(spacerItem)
            for j in range(7):
                chess_path = Path_img + 'none.png'
                chess_name=""

                color=QColor(77,78,81)
                for item in hero_location:
                    if item['location']=="":

                        continue
                    pos = item['location'].split(',')
                    if int(pos[0])-1==i and int(pos[1])-1==j:
                        try:
                            chess_data = chessId_get_data(chess_list, item['hero_id'])
                        except:
                            continue
                        if chess_data["price"] == '1':
                            color = QColor(152,152,152)
                        elif chess_data["price"] == '2':
                            color = QColor(88,177,55)
                        elif chess_data["price"] == '3' or chess_data["price"] == '6':
                            color = QColor(54,120,200)
                        elif chess_data["price"] == '4' or chess_data["price"] == '7':
                            color = QColor(200,31,200)
                        else:
                            color = QColor(253,188,3)

                        chess_name=chess_data["displayName"]
                        chess_path = Path_chess+chess_data['name']
                        break
                frame_chess = QFrame(self.frame)

                lb_chess_ico=HexagonLabel(frame_chess,color,5)
                lb_chess_ico.setAlignment(Qt.AlignCenter)  # 文本居中
                lb_chess_ico.setMaximumSize(int(70*ratio), int(70*ratio))
                lb_chess_ico.setMinimumSize(int(70*ratio), int(70*ratio))
                lb_chess_ico.setScaledContents(True)
                lb_chess_ico.setPixmap(QPixmap(chess_path))
                if chess_path != Path_img + 'none.png':
                    lb_name = QLabel(frame_chess)
                    if "阿卡丽" in chess_name:  # 名字太长处理一下
                        chess_name = "阿卡丽"
                    lb_name.setText(chess_name)
                    lb_name.setObjectName("lb_chess_name2")
                    lb_name.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    lb_name.resize(int(70*ratio), int(20*ratio))
                    lb_name.move(0, int(50 * ratio))
                    self.setStyleSheet(f"""
                        #lb_chess_name2{{
                         color: rgb(255, 255, 255);
                         background: rgba(0, 0, 0, 150);
                        font-family: {setting.font.family()}; 
                        font-size: {setting.font.pointSize()-1}pt                   
                        }}
                        """ )



                h_box.addWidget(frame_chess)
            if i==0 or i==2:
                spacerItem = QSpacerItem(int(40*ratio), int(10*ratio))
                h_box.addItem(spacerItem)
            self.v_box.addLayout(h_box)
