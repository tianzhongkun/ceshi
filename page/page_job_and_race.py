from PyQt5.Qt import *

import setting
from tft import tft
from tools.utils import clear_layout, chessId_get_data, equipId_get_data, job_get_background_sf, race_get_background_sf
from ui.form_job_and_race import Ui_FormJobAndRace
from page.page_item_job_and_race import ItemJobAndRace
class FormJobAndRace(QWidget, Ui_FormJobAndRace):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(744, 95)  # 大小
        self.move(0, 0)  # 位置
        self.frame.setObjectName("frame_box")
        self.v_box=QVBoxLayout(self.frame)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 第一顺位
        # self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setVisible(True)
        # self.setWindowOpacity(0.8)  # 设置1-0之间设置窗口透明度
    def set_ui(self):
        pass
    def add_job_and_race(self,row,_type="job",id="0",num="1"):

        if setting.mode == 1:

            race_list=tft.race_list
            job_list=tft.job_list
        else:

            race_list = tft.race_list2
            job_list = tft.job_list2

        if _type=="job":
            _data=job_get_background_sf(job_list, id,num)
        else:
            _data = race_get_background_sf(race_list, id,num)

        if _data is None:
            return 0
        item_chess=ItemJobAndRace(self)
        item_chess.set_job_and_race(_data,num)
        if _type=="job":
            self.v_box.addWidget(item_chess)
        else:
            self.v_box.addWidget(item_chess)
        return 1
    def set_job_and_race(self,strategy=None):
        '''
        根据攻略数据 分析出来羁绊和职业的激活数量,并且展示
        :param strategy:
        :return:
        '''

        if strategy is None:
            return
        # 清空h_box
        clear_layout(self.v_box)
        if setting.mode == 1:
            chess_list = tft.chess_list
            equip_list=tft.equip_list

        else:
            chess_list = tft.chess_list2
            equip_list = tft.equip_list2

        hero_location=strategy['detail']['hero_location']
        job_list = []
        race_list = []
        for item in hero_location:
            #统计阵容里面的棋字 job和race的数量
            try:
                chess_data = chessId_get_data(chess_list, item['hero_id'])
                if chess_data is None:
                    continue
            except:
                continue
            try:
                job_list+=chess_data['jobIds'].split(',')
            except:
                pass
            try:
                race_list+=chess_data['raceIds'].split(',')
            except:
                pass
            # 看看装备里是否有转职和羁绊
            if item['equipment_id'] != '':
                for equi in item['equipment_id'].split(','):

                    # 将羁绊和职业数据存进容器
                    try:
                        equi_data = equipId_get_data(equip_list, equi)
                        if equi_data is None:  # 排除错误
                            continue
                        if equi_data['jobId'] != '0' and equi_data['jobId'] is not None:
                            job_list.append(equi_data['jobId'])
                    except:
                        pass
                    try:
                        if equi_data['raceId'] != '0' and equi_data['raceId'] is not None:
                            race_list.append(equi_data['raceId'])
                    except:
                        pass

        # 统计职业并按数量降序排序
        job_ss = sorted({}.fromkeys(job_list).keys(),
                        key=lambda x: job_list.count(x),
                        reverse=True)
        row=0


        for job_id in job_ss:
            num=job_list.count(job_id)
            row+=self.add_job_and_race(row,"job",job_id, num)

        # 统计种族并按数量降序排序
        race_ss = sorted({}.fromkeys(race_list).keys(),
                         key=lambda x: race_list.count(x),
                         reverse=True)

        for race_id in race_ss:
            num = race_list.count(race_id)
            row+=self.add_job_and_race(row,"race", race_id, num)



