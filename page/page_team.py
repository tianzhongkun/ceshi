from random import randint
from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import *

from tools.utils import clear_layout
from ui.form_team import Ui_FormTeam
from page.page_item_chess import ItemChess
class FormTeam(QWidget, Ui_FormTeam):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(744, 95)  # 大小
        self.move(0, 0)  # 位置
        self.frame.setObjectName("frame_box")
        self.chess_datas=[]
        #self.frame.setStyleSheet()  # 可以调整为任何背景颜色
        # self.setAutoFillBackground(True)#设置背景为不透明
        #self.tw_strategy_list.setStyleSheet()  # 可以调整为任何背景颜色
        # self.setWindowOpacity(0.5)#设置1-0之间设置窗口透明度
        # # 禁止编辑
        # self.tw_strategy_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # # 水平表格头显示和隐藏
        # self.tw_strategy_list.horizontalHeader().setVisible(False)
        # # 垂直表格头显示和隐藏
        # self.tw_strategy_list.verticalHeader().setVisible(False)
        # # 隐藏分割线
        # self.tw_strategy_list.setShowGrid(False)
        # # 隐藏滚动条
        # self.tw_strategy_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.tw_strategy_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.tw_strategy_list.setRowCount(1)
    def set_ui(self):
        pass
    def add_team(self,chess_id="",chess_name="",chess_level="1",chess_price="1"):
        #增加一行
        # new_col_index = self.tw_strategy_list.columnCount()
        # self.tw_strategy_list.insertColumn(new_col_index)

        item_chess=ItemChess(self)
        item_chess.set_chess(chess_id,chess_name,chess_level,chess_price)
        self.h_box.addWidget(item_chess)
        # self.tw_strategy_list.setCellWidget(0, new_col_index, item_chess)
        # self.tw_strategy_list.resizeColumnsToContents()
    def set_teams(self,chess_datas:list):
        '''
        设置队伍
        :param chess_datas:
        :return:
        '''

        if len(chess_datas)==0:
            return
        self.chess_datas=chess_datas
        # 清空h_box
        clear_layout(self.h_box)
        for item in chess_datas:
            self.add_team(item['chess_id'],item['chess_name'],item['chess_level'],item['chess_price'])
    def test(self):
        '''
        测试展示
        :return:
        '''
        for i in range(10):
            self.add_team(f"{10120+i}",f"懒人",randint(1,3),randint(1,5))




