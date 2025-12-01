from PyQt5.Qt import *
from PyQt5.QtCore import *
from ui.item_job_and_race import Ui_ItemJobAndRace
import setting
class ItemJobAndRace(QWidget, Ui_ItemJobAndRace):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.frame_ico.setMaximumSize(int(25 * setting.ratio), int(30 * setting.ratio))
        self.frame_ico.setMinimumSize(int(25 * setting.ratio), int(30 * setting.ratio))

        self.lb_background = QLabel(self.frame_ico)
        self.lb_background.move(0, 0)
        self.lb_background.setScaledContents(True)
        self.lb_background.setMaximumSize(int(25 * setting.ratio), int(30 * setting.ratio))
        self.lb_background.setMinimumSize(int(25 * setting.ratio), int(30 * setting.ratio))

        self.lb_ico=QLabel(self.frame_ico)
        self.lb_ico.move(int(3 * setting.ratio),int(5 * setting.ratio))
        self.lb_ico.setScaledContents(True)
        self.lb_ico.setMaximumSize(int(19 * setting.ratio), int(19 * setting.ratio))
        self.lb_ico.setMinimumSize(int(19 * setting.ratio), int(19 * setting.ratio))

        self.lb_name.setObjectName("lb_title")

        #self.frame.addWidget(self.lb_background,self.lb_ico)
    def set_ui(self):
        pass
    def set_job_and_race(self,_data,num=1):
        """
        根据职业或者羁绊 id 显示图标  和激活数量
        :return:
        """
        self.lb_background.setPixmap(QPixmap(_data[0]))
        self.lb_ico.setPixmap(QPixmap(_data[1]))
        self.lb_name.setText(f" {num} {_data[2]['name']}")
        ttt=str(_data[2]['level']).replace(', \'', '<br>').replace('\n','').replace('\'', '').replace('{', '').replace('}', '')
        txt_tool=f"""<h2 style="color:#FFFFFF;text-align:center;">{num} {_data[2]['name']}</h2>
            <h3 style="color:#825418;"> {_data[2]['introduce']}</h2>
                
                        <h4 style="color:#E7E7E9;">
                        {ttt}
                        </h2>"""
        self.lb_name.setToolTip(txt_tool)
        self.lb_ico.setToolTip(txt_tool)

