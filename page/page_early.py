from PyQt5 import QtCore
from PyQt5.Qt import *

import setting
from setting import ratio, Path_img, Path_chess
from tft import tft
from tools.utils import clear_layout, chessId_get_data
from ui.form_early import Ui_FormEarly
from page.page_item_chess import ItemChess
class FormEarly(QWidget, Ui_FormEarly):
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
        self.setWindowOpacity(0.8)  # 设置1-0之间设置窗口透明度
        self.h_box_list = []  # 横向的
    def set_ui(self):
        pass
    def set_early(self,strategy=None):
        if strategy is None:
            return
        # 清空box
        clear_layout(self.v_box)
        early_heros = strategy['detail']['y21_early_heros']
        metaphase_heros = strategy['detail']['y21_metaphase_heros']
        hero_replace=strategy['detail']['hero_replace']
        self.h_box_list = []  # 横向的
        # 前期列表
        if early_heros != '':
            self.__add_heros(early_heros,"前期")
        # 中期列表
        if metaphase_heros != '':
            self.__add_heros(metaphase_heros, "中期")
        # 备选
        if hero_replace != '':
            for hero_rep in hero_replace:
                self.__add_heros_replace(hero_rep)
        # 后面添加一个弹簧
        spacerItem = QSpacerItem(int(5 * ratio), int(5 * ratio), QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.v_box.addItem(spacerItem)
    def __add_heros(self,early_heros,title="前期"):

        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        h_box.setSpacing(int(13 * ratio))

        lb_title = QLabel(title, self.frame)
        lb_title.setObjectName('lb_title')
        h_box.addWidget(lb_title)

        # 开始遍历列表
        for item in early_heros:
            chess_id = item['hero_id']
            self.__add_hero(chess_id, h_box)
        #后面添加一个弹簧

        spacerItem = QSpacerItem(int(5 * ratio), int(5 * ratio),QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_box.addItem(spacerItem)

        self.h_box_list.append(h_box)
        self.v_box.addLayout(h_box)
    def __add_heros_replace(self,hero_rep,):
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        h_box.setSpacing(int(10 * ratio))

        lb_title = QLabel("备选", self.frame)
        lb_title.setObjectName('lb_title')
        h_box.addWidget(lb_title)


        for chess_id in hero_rep['hero_id'].split(','):
            self.__add_hero(chess_id,h_box)
        # 中间的指针箭头
        lb_jt= QLabel(" > ", self.frame)
        lb_jt.setObjectName('lb_title')
        h_box.addWidget(lb_jt)

        for chess_id in hero_rep['replace_heros'].split(','):
            self.__add_hero(chess_id,h_box)
        #后面添加一个弹簧

        spacerItem = QSpacerItem(int(5 * ratio), int(5 * ratio),QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_box.addItem(spacerItem)

        self.h_box_list.append(h_box)
        self.v_box.addLayout(h_box)
    def __add_hero(self,chess_id="",h_box=None):
        if setting.mode == 1:
            chess_list = tft.chess_list
        else:
            chess_list = tft.chess_list2
        try:
            chess_data = chessId_get_data(chess_list, chess_id)
        except:
            return
        chess_level = 1
        item_chess = ItemChess(self.frame)
        item_chess.set_chess(chess_id=chess_id, chess_name=chess_data["displayName"],
                             chess_level=chess_level, chess_price=chess_data['price'])
        item_chess.frame_chess.setFixedSize(int(52 * setting.ratio), int(60 * setting.ratio))
        item_chess.lb_chess_ico.resize(int(50 * setting.ratio), int(50 * setting.ratio))
        item_chess.lb_chess_name.move(0, int(52 * setting.ratio) - int(20 * setting.ratio))  # 位置
        item_chess.lb_chess_name.resize(int(52 * setting.ratio), int(20 * setting.ratio))
        item_chess.lb_chess_name.setStyleSheet(f""" 
                                                                     color: rgb(255, 255, 255);
                                                                     background: rgba(0, 0, 0, 150);
                                                                    font-family: {setting.font.family()}; 
                                                                    font-size: {setting.font.pointSize() - 4}pt                   
                                                                    """)
        h_box.addWidget(item_chess)
