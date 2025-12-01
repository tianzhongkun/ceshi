from PyQt5.Qt import *
from tft import tft
from tools.utils import tanChudataForm, chessId_get_data
from ui.item_chess import Ui_ItemChess
import setting
class ItemChess(QWidget, Ui_ItemChess):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)

        self.frame_chess.setFixedSize(int(72*setting.ratio), int(90*setting.ratio))
        self.move(0, 0)  # 位置
        self.lb_chess_ico.resize(int(70*setting.ratio), int(70*setting.ratio))
        self.lb_chess_ico.move(int(0*setting.ratio), int(0*setting.ratio))  # 位置
        self.lb_chess_ico.setObjectName("lb_chess_ico")
        self.frame_chess.setObjectName("frame_chess")
        self.lb_chess_level.setObjectName("lb_chess_level")
        self.lb_chess_level.move(0, 0)  # 位置
        self.lb_chess_level.resize(int(72 * setting.ratio), int(15 * setting.ratio))

        self.lb_chess_name.setObjectName("lb_chess_name")
        self.lb_chess_name.move(0, int(85*setting.ratio)-int(20 * setting.ratio))  # 位置
        self.lb_chess_name.resize(int(72 * setting.ratio), int(20 * setting.ratio))
        #self.frame.setStyleSheet()  # 可以调整为任何背景颜色
        # self.setAutoFillBackground(True)#设置背景为不透明
        #self.tw_strategy_list.setStyleSheet()  # 可以调整为任何背景颜色
        # self.setWindowOpacity(0.5)#设置1-0之间设置窗口透明度
    def set_ui(self):
        pass
    def set_chess(self,chess_id="",chess_name="", chess_level="1",chess_price="1"):
        """
        设置棋子属性
        :param chess_id:
        :param chess_price:
        :param chess_name:
        :param chess_ico:
        :param chess_level:
        :return:
        """
        if chess_level=="3":
            self.lb_chess_level.setText("★★★")
        else:
            self.lb_chess_level.setText("")
        if len(chess_name)>4:#名字太长处理一下
            chess_name=chess_name[:4]

        if setting.mode==1:
            chess_list=tft.chess_list
            job_list = tft.job_list
            race_list=tft.race_list
        else:
            chess_list = tft.chess_list2
            job_list = tft.job_list2
            race_list = tft.race_list2
        self.lb_chess_name.setText(chess_name)


        chess_data=chessId_get_data(chess_list, chess_id)
        chess_ico = f"datas/chess/{chess_data['name']}"
        self.lb_chess_ico.setScaledContents(True)

        self.lb_chess_ico.setPixmap(QPixmap(chess_ico))
        txt_tool=tanChudataForm(chess_data, job_list, race_list)
        self.lb_chess_ico.setToolTip(txt_tool)
        self.lb_chess_level.setToolTip(txt_tool)
        self.lb_chess_name.setToolTip(txt_tool)
        if chess_price== "1":
            color = '#989898'
        elif chess_price == "2":
            color = '#58B137'
        elif chess_price == "3" or chess_price == "6":
            color = '#3678C8'
        elif chess_price == "4" or chess_price == "7":
            color = '#C81FC8'
        else:
            color = '#FDBC03'
        if chess_ico != setting.Path_img + 'none.png':
            self.lb_chess_ico.setStyleSheet('''#lb_chess_ico{border: 2px solid %s;  }''' % color)

        # self.lb_chess_ico.setStyleSheet(f"background-image: url({chess_ico});")




