from PyQt5.Qt import *
from tft import tft
from tools.utils import  tanChu_EquipData, equipId_get_data
from ui.item_equip import Ui_ItemEquip
import setting
class ItemEquip(QWidget, Ui_ItemEquip):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(int(72*setting.ratio), int(72*setting.ratio))  # 大小
        self.setFixedSize(int(72*setting.ratio), int(72*setting.ratio))
        self.frame.setFixedSize(int(72*setting.ratio), int(72*setting.ratio))
        self.frame.setObjectName("frame_chess")
        self.move(0, 0)  # 位置
        self.lb_big.setScaledContents(True)
        self.lb_big.setMaximumSize(int(45*setting.ratio), int(45*setting.ratio))

        self.lb_samll1.setScaledContents(True)
        self.lb_samll1.setMaximumSize(int(20 * setting.ratio), int(20 * setting.ratio))

        self.lb_samll2.setScaledContents(True)
        self.lb_samll2.setMaximumSize(int(20 * setting.ratio), int(20 * setting.ratio))

        self.lb_samlls=[self.lb_samll1,self.lb_samll2]


    def set_ui(self):
        pass
    def set_equip(self,equip_data=None):
        """
        设置推荐装备
        :param equip_data:
        :return:
        """

        if equip_data is not None:

            txt_tool=tanChu_EquipData(tft.equip_list, equip_data)
            self.lb_big.setToolTip(txt_tool)
            path_big_img=setting.Path_equip + equip_data['imagePath'].split('/')[-1]


            self.lb_big.setPixmap(QPixmap(path_big_img))
            samll_datas=equip_data['formula'].split(',')
            for i in range(len(samll_datas)):
                try:
                    equip_samll_data = equipId_get_data(tft.equip_list, samll_datas[i])
                    path_samll_img =setting.Path_equip + equip_samll_data['imagePath'].split('/')[-1]
                    self.lb_samlls[i].setPixmap(QPixmap(path_samll_img))
                except:
                    pass









