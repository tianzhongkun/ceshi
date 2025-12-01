from PyQt5.Qt import *

import setting
from ui.form_doc import Ui_FormDoc
class FormDoc(QWidget, Ui_FormDoc):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        #鼠标穿透 这3个配套的
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 第一顺位
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.75)  # 设置1-0之间设置窗口透明度
        self.setVisible(True)

        self.frame.setObjectName("frame_doc")
        self.lb_doc.setObjectName("lb_doc")
        self._typer="早期"
        self.doc_early=""
        self.doc_d_time= ""
        self.doc_enemy= ""
        self.doc_location=""



    def set_ui(self):
        pass
    def switch_doc(self,_typer="早期"):
        window_main = self.parent()
        self._typer=_typer
        if _typer=="早期":
            self.lb_doc.setText(self.doc_early)
        elif _typer=="D牌":
            self.lb_doc.setText(self.doc_d_time)
        elif _typer=="克制":
            self.lb_doc.setText(self.doc_enemy)
        elif _typer=="站位":
            self.lb_doc.setText(self.doc_location)
        self.setMaximumHeight(int(setting.ratio * 176))
        self.frame.setMaximumHeight(int(setting.ratio * 176))
        self.adjustSize()

        self.move(setting.p_left + window_main.width() - self.width() - int(setting.ratio * 68),
                  setting.p_top + int(setting.ratio * 60))
    def set_doc(self,strategy=None):

        self.doc_early =strategy['detail']['early_info'].replace("&#10;", "")+"。"+strategy['detail']['equipment_info'].replace('&amp;nbsp;','').replace("&#10;","")
        self.doc_d_time = strategy['detail']['d_time'].replace("&#10;", "")
        self.doc_enemy =strategy['detail']['enemy_info'].replace("&#10;", "")
        self.doc_location = strategy['detail']['location_info'].replace("&#10;", "")
        self.switch_doc(self._typer)












