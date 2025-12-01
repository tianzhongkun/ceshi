import random
import traceback

import setting
from tft import  tft
from PyQt5.Qt import *
from tools.utils import chessId_get_data
from ui.item_strategy import Ui_ItemStrategy

class ItemStrategy(QWidget, Ui_ItemStrategy):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(int(740*setting.ratio), int(56*setting.ratio))  # 大小
        self.setFixedSize(int(740*setting.ratio), int(56*setting.ratio))
        self.frame.setFixedSize(int(740*setting.ratio), int(56*setting.ratio))
        self.lb_tphot.setMaximumSize(int(50*setting.ratio), int(50*setting.ratio))
        self.lb_tphot.setMinimumSize(int(50 * setting.ratio), int(50 * setting.ratio))
        self.lb_title.setObjectName("lb_title")
        self.move(0, 0)  # 位置
        self.strategy=None
    def set_ui(self):
        pass
    def set_strategy(self,strategy=None):
        """
        设置攻略
        :return:
        """
        if strategy is None:
            self.lb_tphot.setScaledContents(True)
            if random.randint(0, 1) == 1:
                self.lb_tphot.setPixmap(QPixmap(setting.Path_img + "A.png"))
            else:
                self.lb_tphot.setPixmap(QPixmap(setting.Path_img + "S.png"))
            self.lb_title.setText("【猛拍按钮专属】6堡垒卫士4赛博老大2高级工程师"+"x"*random.randint(1,10))
        else:
            self.strategy = strategy
            self.lb_tphot.setScaledContents(True)
            if strategy['quality']== "A":
                self.lb_tphot.setPixmap(QPixmap(setting.Path_img + "A.png"))
            elif  strategy['quality'] == "S":
               self.lb_tphot.setPixmap(QPixmap(setting.Path_img + "S.png"))
            else:
                # 创建并配置字体
                font = QFont()
                font.setFamily("Arial")  # 设置字体
                font.setPointSize(int(13*setting.ratio))  # 设置字号
                font.setBold(True)  # 设置粗体
                font.setWeight(QFont.Bold)  # 设置字体粗细（可选）
                pixmap = QPixmap(setting.Path_img + "X.png")
                painter = QPainter(pixmap)
                painter.setPen(QColor(219,158,80))  # 文字颜色
                painter.setFont(font)  # 应用字体
                painter.drawText(pixmap.rect(), Qt.AlignCenter, strategy['quality'])
                painter.end()
                self.lb_tphot.setPixmap(pixmap)


            self.lb_title.setText(strategy['detail']['line_name'])
    def update_item(self,mode=1):
        hero_location = self.strategy['detail']['hero_location']
        level_3_heros = self.strategy['detail']['level_3_heros']
        chess_datas = []

        if mode==1:
            chess_list=tft.chess_list
        else:
            chess_list = tft.chess_list2

        for heroitem in hero_location:
            try:
                if heroitem['chess_type'] != 'hero':
                    continue

                chess_data = chessId_get_data(chess_list, heroitem['hero_id'])

            except:
                traceback.print_exc()
                continue



            d = {'chess_id': heroitem['hero_id'], 'chess_name': chess_data["displayName"],
                 'chess_level': "3" if heroitem['hero_id'] in level_3_heros else "1",
                 'chess_price': chess_data["price"]}
            chess_datas.append(d)

        window_main=self.parent().parent().parent().parent().parent()
        window_main.window_team.set_teams(chess_datas)
        window_main.window_job_and_race.set_job_and_race(self.strategy)
        window_main.window_equip.set_equips(self.strategy)
        window_main.window_doc.set_doc(self.strategy)
        window_main.window_location.set_location(self.strategy)
        window_main.window_early.set_early(self.strategy)

        #print(self.strategy)









