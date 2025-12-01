import threading
import webbrowser
from PyQt5.Qt import *
from PyQt5.QtCore import *
import setting
from tft import tft_encrypt_to_str
from tools.utils import chess_id_to_tftid
from ui.form_nav import Ui_FormNav
class FormNav(QWidget, Ui_FormNav):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(224, 88)  # 大小
        self.move(200, 200)  # 位置
        self.frame.setObjectName("frame_box")
        self.bt_sponsorship.clicked.connect(lambda: webbrowser.open(setting.sponsorship_url) )
        self.clipboard = QApplication.clipboard()
    def set_ui(self):
        pass
    @pyqtSlot()  # 装饰器，用于指定信号处理函数的参数类型 防止重复触发
    def on_bt_strategy_clicked(self):
        self.parent().window_strategy_list.setVisible(not self.parent().window_strategy_list.isVisible())
        self.parent().window_job_and_race.setVisible(not self.parent().window_job_and_race.isVisible())


        if self.parent().window_strategy_list.isVisible():
            if setting.mode == 2:
                setting.mode = 1
                self.parent().load_strategy_list(setting.mode)

    @pyqtSlot()  # 装饰器，用于指定信号处理函数的参数类型 防止重复触发
    def on_bt_strategy2_clicked(self):

        self.parent().window_strategy_list.setVisible(not self.parent().window_strategy_list.isVisible())
        self.parent().window_job_and_race.setVisible(not self.parent().window_job_and_race.isVisible())

        if self.parent().window_strategy_list.isVisible():
            if setting.mode == 1:
                setting.mode = 2
                self.parent().load_strategy_list(setting.mode)
    @pyqtSlot()  # 装饰器，用于指定信号处理函数的参数类型 防止重复触发
    def on_bt_confirmed_clicked(self):

        if setting.mode==1:
            id_list = [int(item['chess_id']) for item in self.parent().window_team.chess_datas]
            tft_str = tft_encrypt_to_str(id_list,mode=setting.mode)
        else:

            id_list = [int(chess_id_to_tftid(self.parent().tft.chess_list2, item['chess_id'])) for item in self.parent().window_team.chess_datas]
            tft_str = tft_encrypt_to_str(id_list,mode=setting.mode)
        self.clipboard.setText(tft_str)
        if len(id_list)<=0 or self.parent().auto_tft.moni.hwnd==0:
            self.parent().on_show_log("请先运行游戏,点击这个后会自动把阵容复制到官方的小队规划里",(255,0,0),1000)
            return

        threading.Thread(target=self.parent().auto_tft.click_confirmed,daemon=True).start()






