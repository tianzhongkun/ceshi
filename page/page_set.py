from PyQt5.Qt import *
import setting
from ui.form_set import Ui_FormSet
class FormSet(QWidget, Ui_FormSet):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(260, 88)  # 大小
        self.move(200, 200)  # 位置
        self.frame.setObjectName("frame_box")

    def set_ui(self):
        pass
    @pyqtSlot(int)
    def on_cb_equip_stateChanged(self,index):
        if index==0:
            self.parent().window_equip.setVisible(False)
        else:
            self.parent().window_equip.setVisible(True)


    @pyqtSlot(int)
    def on_cb_location_stateChanged(self, index):

        if index == 0:
            self.parent().window_location.setVisible(False)
            self.parent().window_early.setVisible(False)

        else:
            self.parent().window_location.setVisible(True)
            #self.parent().window_early.setVisible(True)

    @pyqtSlot(int)
    def on_cb_auto_start_stateChanged(self, index):
        if index == 0:
            self.parent().auto_tft.is_auto_start = False
        else:
            self.parent().auto_tft.is_auto_start = True

    @pyqtSlot(int)
    def on_cb_side_stateChanged(self, index):
        if index == 0:
            self.parent().auto_tft.is_side = False
        else:
            self.parent().auto_tft.is_side = True







