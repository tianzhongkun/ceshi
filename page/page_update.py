import subprocess
import time
from PyQt5.Qt import *

import setting
from ui.form_update import Ui_FormUpdate
class FormUpdate(QDialog, Ui_FormUpdate):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget | Qt.WindowStaysOnTopHint)  # 风格
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowOpacity(1.0)#设置1-0之间设置窗口透明度
        self.setWindowIcon(QIcon("datas/img/logo.png"))
        self.frame.setObjectName("frame_box")
        self.lb_title.setObjectName("lb_title")
        self.setStyleSheet(
            "font-family: {}; font-size: {}pt;".format(setting.font.family(), setting.font.pointSize()+7))
        self.resize(int(setting.ratio*800),int(setting.ratio*500))

        self.new_ver = "1.0"
        self.url = ""
        self.min_ver = "0.0"
        self.name = "LRTFT"
        self.is_exit=False
    def set_ui(self):
        pass
    def set_update(self,update_info="",title="发现新版本,是否更新?",name="",url="",min_ver="0.0"):
        self.url=url
        self.min_ver=min_ver
        self.name=name
        self.pte_update_txt.setPlainText(update_info)
        if float(setting.ver) >= float(min_ver):
            self.lb_title.setText(title)

        else:
            title=f"当前版本低于 V{min_ver} 不支持自动更新请手动去下载最新的 一键安装包"
            self.bt_yes.setEnabled(False)
        self.lb_title.setText(title)

    @pyqtSlot()
    def on_bt_no_clicked(self):
        self.is_exit = False
        self.close()


    @pyqtSlot()
    def on_bt_yes_clicked(self):
        subprocess.Popen(f'update.exe "{self.name}" "{self.url}"',creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)
        self.is_exit=True
        self.close()















