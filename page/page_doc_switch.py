from PyQt5.Qt import *
from PyQt5.QtCore import *
from ui.form_doc_switch import Ui_FormDocSwitch
class FormDocSwitch(QWidget, Ui_FormDocSwitch):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(224, 88)  # 大小
        self.move(200, 200)  # 位置
        self.frame.setObjectName("frame_box")
        self.bt_close.clicked.connect(lambda: self.parent().close())
    def switch_doc(self,_typer="早期"):
        window_main = self.parent()

        visible = window_main.window_doc.isVisible()

        if visible:
            if window_main.window_doc._typer == _typer:
                window_main.window_doc.setVisible(False)
        else:
            window_main.window_doc.setVisible(True)


        window_main.window_doc.switch_doc(_typer)
    @pyqtSlot()
    def on_bt_early_clicked(self):
        self.switch_doc("早期")
        window_main = self.parent()
        visible = window_main.window_doc.isVisible()
        if visible:
            window_main.window_early.setVisible(True)
            window_main.window_set.cb_location.setChecked(True)
            window_main.window_location.setVisible(False)
        else:
            window_main.window_set.cb_location.setChecked(True)
            window_main.window_early.setVisible(False)
            window_main.window_location.setVisible(True)
    @pyqtSlot()
    def on_bt_d_time_clicked(self):
        self.switch_doc("D牌")
    @pyqtSlot()
    def on_bt_enemy_clicked(self):
        self.switch_doc("克制")
    @pyqtSlot()
    def on_bt_location_clicked(self):
        self.switch_doc("站位")
        window_main = self.parent()
        visible = window_main.window_doc.isVisible()
        if visible:
            window_main.window_set.cb_location.setChecked(True)
            window_main.window_location.setVisible(True)
            window_main.window_early.setVisible(False)
    def set_ui(self):
        pass


