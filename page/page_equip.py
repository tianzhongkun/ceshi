from PyQt5.Qt import *
import setting
from page.page_item_chess import ItemChess
from page.page_item_equip import ItemEquip
from tft import tft
from tools.utils import clear_layout, chessId_get_data, equipId_get_data, job_get_background_sf, race_get_background_sf
from ui.form_equip import Ui_FormEquip
from page.page_item_job_and_race import ItemJobAndRace
class FormEquip(QWidget, Ui_FormEquip):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(340, 400)  # 大小
        self.move(0, 0)  # 位置
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 第一顺位
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景支持
        self.setVisible(True)
        # self.frame.setAttribute(Qt.WA_TranslucentBackground, True)  # 透明背景支持
        self.setWindowOpacity(0.7)  # 设置1-0之间设置窗口透明度
        self.frame.setObjectName("frame_box")
        self.v_box=QVBoxLayout(self.frame)

        self.v_box.setAlignment(Qt.AlignTop)  # 顶部对齐
        self.v_box.setContentsMargins(0, 0, 0, 0)
        self.v_box.setSpacing(0)
    def set_ui(self):
        pass
    def add_equip(self,row,_type="job",id="0",num="1"):
        if _type=="job":
            _data=job_get_background_sf(tft.job_list, id,num)
        else:
            _data = race_get_background_sf(tft.race_list, id,num)
        if _data is None:
            return 0
        item_chess=ItemJobAndRace(self)
        item_chess.set_job_and_race(_data,num)
        if _type=="job":
            self.v_box.addWidget(item_chess)
        else:
            self.v_box.addWidget(item_chess)
        return 1
    def set_equips(self,strategy=None):
        '''
        根据攻略数据 分析出来羁绊和职业的激活数量,并且展示
        :param strategy:
        :return:
        '''

        if strategy is None:
            return
        if setting.mode == 1:
            chess_list = tft.chess_list
            equip_list = tft.equip_list

        else:
            chess_list = tft.chess_list2
            equip_list = tft.equip_list2

        # 清空h_box
        clear_layout(self.v_box)

        txt_tool=f"""<h2 style="color:#E7E7E9;"> {strategy['detail']['equipment_info'].replace('&amp;nbsp;','')}</h2>""".replace("&#10;","\n")
        self.frame.setToolTip(txt_tool)
        hero_location=strategy['detail']['hero_location']
        level_3_heros = strategy['detail']['level_3_heros']
        for heroitem in hero_location:
            if heroitem['equipment_id'] != '':
                try:
                    chess_data = chessId_get_data(chess_list, heroitem['hero_id'])
                except:
                    continue
                d = {'chess_id': heroitem['hero_id'],
                     'chess_name': chess_data["displayName"],
                     'chess_level': "3" if heroitem['hero_id'] in level_3_heros else "1",
                     'chess_price': chess_data["price"]}
                item_frame = QFrame(self.frame)
                item_h_box=QHBoxLayout(item_frame)
                item_h_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
                item_h_box.setContentsMargins(0, 0, 0, 0)
                item_h_box.setSpacing(0)
                item_chess = ItemChess(item_frame)
                item_chess.set_chess(d['chess_id'],d['chess_name'],d['chess_level'],d['chess_price'])
                item_chess.lb_chess_name.move(0, int(85 * setting.ratio) - int(35 * setting.ratio))  # 位置

                item_h_box.addWidget(item_chess)
                lb_jt=QLabel(" > ",item_frame)
                lb_jt.setObjectName("lb_jt")
                lb_jt.setStyleSheet(f"""#lb_jt {{
                      color: rgb(255,255,97);
                      font-family: {setting.font.family()}; 
                      font-size: {setting.font.pointSize()+5}pt;
                    }}""")
                item_h_box.addWidget(lb_jt)

                for equi in heroitem['equipment_id'].split(','):
                    try:
                        equip_data = equipId_get_data(equip_list, equi)
                        if equip_data is None:  # 排除错误
                            continue
                        item_equip = ItemEquip(item_frame)
                        item_equip.set_equip(equip_data)
                        item_h_box.addWidget(item_equip)
                    except:
                        pass

                self.v_box.addWidget(item_frame)






