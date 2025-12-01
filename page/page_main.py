import json
import os
import sys
import threading
import webbrowser

import setting
import requests
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from auto_tft import AutoTFT
from moni.hook_key_mouse import HookKeyMouse
from moni.moni import MoNi
from page.page_doc import FormDoc
from page.page_doc_switch import FormDocSwitch
from page.page_early import FormEarly
from page.page_equip import FormEquip
from page.page_job_and_race import FormJobAndRace
from page.page_location import FormLocation
from page.page_nav import FormNav
from page.page_set import FormSet
from page.page_show_log import ShowLog
from page.page_strategy_list import FormStrategyList
from page.page_team import FormTeam
from tft import  tft
from tools.utils import CreateNewImage
from ui.main import Ui_MainWindow
class MySignals(QObject):
    hide_ui = pyqtSignal()
    show_log = pyqtSignal(str,tuple,int)
    switch_id=pyqtSignal(bool)
    update_ui = pyqtSignal(int,int)
class main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget | Qt.WindowStaysOnTopHint)#风格
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        #self.setWindowOpacity(1.0)#设置1-0之间设置窗口透明度
        self.setWindowIcon(QIcon("datas/img/logo.png"))
        # 保持全屏置顶
        self.setGeometry(0, 0, setting.window_width, setting.window_height)
        self.setWindowTitle('LRTFT' + setting.ver)  # 标题
        self.strategy=None
        # 子窗口
        self.window_nav = FormNav(self)
        self.window_set =FormSet(self)
        self.window_team = FormTeam(self)
        self.window_strategy_list = FormStrategyList(self)
        self.window_job_and_race=FormJobAndRace(self)
        self.window_equip=FormEquip(self)
        self.window_doc = FormDoc(self)
        self.window_doc_switch=FormDocSwitch(self)
        self.window_location=FormLocation(self)
        self.window_early=FormEarly(self)
        self.tft = tft
        self.down_imgs()
        self.down_imgs(2)

        # 设置字体大小
        self.setStyleSheet(
            "font-family: {}; font-size: {}pt;".format(setting.font.family(), setting.font.pointSize()))
        self.sg=MySignals()
        self.sg.hide_ui.connect(self.on_hide_ui)
        self.sg.show_log.connect(self.on_show_log)
        self.sg.switch_id.connect(self.on_switch_id)
        self.sg.update_ui.connect(self.update_ui)
        moni = MoNi().create(0,  setting.mode_mn)
        self.auto_tft = AutoTFT(moni)
        self.auto_tft.set_sg(self.sg)
        self.auto_tft.get_game_hwnd()
        # 启动全局钩子
        HookKeyMouse.start_global_hook()

        self.show_log=None
        self.load_set()
        self.thread_auto_tft = threading.Thread(target=self.auto_tft.run, daemon=True)
        self.thread_auto_tft.start()
        self.thread_auto_start = threading.Thread(target=self.auto_tft.run_auto_start, daemon=True)
        self.thread_auto_start.start()
    def set_ui(self):
        pass
    @pyqtSlot()
    def on_hide_ui(self):
        try:
            on=self.isMinimized()
            if not on:
                self.showMinimized()
                self.on_show_log("隐藏UI",(255,255,0),1000)
            else:
                self.showNormal()
                self.on_show_log("显示UI",(255,255,0),1000)
        except Exception as e:
            print(e)
            pass
    @pyqtSlot(str,tuple,int)
    def on_show_log(self, log: str,color=[0,0,0],time_end=1000):
        try:
            self.show_log = ShowLog(log,time_end=time_end,color=color)
            self.show_log.show()
        except Exception as e:
            print(e)
            pass
    @pyqtSlot(bool)
    def on_switch_id(self,on:bool):
        row = self.window_strategy_list.tw_strategy_list.currentIndex().row()
        if on:
            next_row = row+ 1
        else:
            next_row = row - 1
        if next_row < 0:
            next_row = 0
        if next_row >= self.window_strategy_list.tw_strategy_list.rowCount():
            next_row = self.window_strategy_list.tw_strategy_list.rowCount() - 1
        self.window_strategy_list.tw_strategy_list.setCurrentCell(next_row, 0)
    @pyqtSlot(int,int)
    def update_ui(self,p_left=0,p_top=0):
        '''
        更新ui
        :return:
        '''
        # 保持全屏置顶
        self.setGeometry(p_left, p_top, setting.window_width, setting.window_height)
        # 设置字体大小
        self.setStyleSheet(
            "font-family: {}; font-size: {}pt;".format(setting.font.family(), setting.font.pointSize()))
        self.sg = MySignals()

        # 成员列表展示
        self.window_team.move(0, 0)
        self.window_team.resize(int(setting.ratio * 740), int(setting.ratio * 100))
        # 导航栏
        self.window_nav.move(int(setting.ratio * 740)-2, 0)
        self.window_nav.resize(int(setting.ratio * 180), int(setting.ratio * 100))

        # 设置栏
        self.window_set.move(int(setting.ratio * 1687) , 0)
        self.window_set.resize(int(setting.ratio * 300), int(setting.ratio * 58))

        # 攻略列表
        self.window_strategy_list.move(0, int(setting.ratio * 100)-2)
        self.window_strategy_list.resize(int(setting.ratio * 550), int(setting.ratio * 260))

        # 设置默认行高为55像素
        self.window_strategy_list.tw_strategy_list.verticalHeader().setDefaultSectionSize(int(setting.ratio * 55))
        self.window_strategy_list.tw_strategy_list.horizontalHeader().setDefaultSectionSize(int(setting.ratio * 505))

        #职业和羁绊展示窗口
        self.window_job_and_race.move(int(setting.ratio * 550),int(setting.ratio * 100)-2)
        self.window_job_and_race.resize(int(setting.ratio * 190), int(setting.ratio * 260))
        self.window_job_and_race.setMaximumSize(int(setting.ratio * 190), int(setting.ratio * 260))

        #装备推荐窗口
        self.window_equip.resize(int(setting.ratio * 344), int(setting.ratio * 440))
        self.window_equip.move(p_left, p_top+self.height()-self.window_equip.height())

        # 攻略文案窗口
        self.window_doc.resize(int(setting.ratio * 800), int(setting.ratio * 176))
        self.window_doc.setMaximumSize(int(setting.ratio * 800), int(setting.ratio * 176))
        self.window_doc.move(p_left+self.width()-self.window_doc.width()-int(setting.ratio * 68), p_top+int(setting.ratio * 60))

        #切换攻略窗口导航
        self.window_doc_switch.resize(int(setting.ratio * 240), int(setting.ratio * 58))

        self.window_doc_switch.move(self.width() - self.window_doc_switch.width() - int(setting.ratio * 38), 0)

        #阵容站位
        self.window_location.resize(int(setting.ratio * 570), int(setting.ratio * 316))
        self.window_location.move(p_left+self.width() - self.window_location.width() ,p_top+self.height() - self.window_location.height() )

        # 早期过渡
        self.window_early.resize(int(setting.ratio * 570), int(setting.ratio * 316))
        self.window_early.move(p_left+self.width() - self.window_early.width(),
                                  p_top+self.height() - self.window_early.height())
        self.window_early.setVisible(False)
        self.window_strategy_list.setVisible(False)
        self.window_job_and_race.setVisible(False)
        self.window_doc.setVisible(False)
    def load_strategy_list(self,mode=1):
        """
        加载官方阵容
        """
        if mode==1:
            self.window_strategy_list.set_teams(self.tft.strategy_list)
        elif mode==2:
            self.window_strategy_list.set_teams(self.tft.strategy_list2)
    def down_imgs(self,mode=1):
        '''
        下载官网的图片数据
        :return:
        '''
        if mode==1:
            chess_list=self.tft.chess_list
            equip_list=self.tft.equip_list
            job_list=self.tft.job_list
            race_list=self.tft.race_list
        else :
            chess_list = self.tft.chess_list2
            equip_list = self.tft.equip_list2
            job_list = self.tft.job_list2
            race_list = self.tft.race_list2
        # '棋子图片'
        for item in chess_list:
            name = item['name']
            Path_1 = f"{setting.Path_chess}/{name}"
            if os.path.exists(Path_1) == False:
                url = f"{setting.chess_url}{name}"
                res = requests.get(url, verify=False)
                with open(Path_1, 'wb') as f:
                    f.write(res.content)

        # # '棋子大图'
        # for item in self.tft.chess_list:
        #     name = item['name'].split('.')[0]
        #     Path_1 = f"{setting.Path_chess_big}/{name}.jpg"
        #     if os.path.exists(Path_1) == False:
        #         url = f"{setting.chess_big_url}{name}.jpg"
        #         res = requests.get(url)
        #
        #         with open(Path_1, 'wb') as f:
        #             f.write(res.content)

        # '装备图片'
        for item in equip_list:
            name = item['imagePath'].split('/')[-1]
            Path_1 = f"{setting.Path_equip}/{name}"
            if os.path.exists(Path_1) == False:
                url = item['imagePath']
                url = url.replace("https", "http")
                res = requests.get(url, verify=False)

                with open(Path_1, 'wb') as f:
                    f.write(res.content)

        # '职业图片'
        for item in job_list:
            try:

                name = item['imagePath'].split('/')[-1]
                Path_1 = f"{setting.Path_job}/{name}"
                if os.path.exists(Path_1) == False:
                    if item['name'] == "召唤物":
                        continue
                    url = item['imagePath']
                    url = url.replace("https", "http")
                    res = requests.get(url)
                    Path_2 = f"{setting.Path_job2}/{name}"
                    with open(Path_2, 'wb') as f:
                        f.write(res.content)
                    # 将图片的颜色转换成白色
                    CreateNewImage(Path_2, Path_1, [255, 255, 255])

            except Exception as err:
                print("职业图片下载失败", err,item)

        #'羁绊图片'
        for item in race_list:
            try:
                name = item['imagePath'].split('/')[-1]
                Path_1 = f"{setting.Path_race}/{name}"
                if not os.path.exists(Path_1):
                    if item['name'] == "召唤物":
                        continue
                    url = item['imagePath']
                    url = url.replace("https", "http")
                    res = requests.get(url, verify=False)

                    Path_2 = f"{setting.Path_race2}/{name}"
                    with open(Path_2, 'wb') as f:
                        f.write(res.content)
                    # 将图片的颜色转换成白色
                    CreateNewImage(Path_2, Path_1, [255, 255, 255])
            except Exception as err:
                print("羁绊图片下载失败", err,item)
    def load_set(self):
        try:
            with open('datas/setting.json', 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

                try:
                    setting.mode = loaded_data['mode']

                except:
                    setting.mode = 1
                try:
                    self.auto_tft.is_side=loaded_data['is_side']

                except:
                    self.auto_tft.is_side =True
                self.window_set.cb_side.setChecked(self.auto_tft.is_side)
                self.load_strategy_list(setting.mode)
                # 定位到最新的索引
                self.window_strategy_list.tw_strategy_list.setCurrentCell(loaded_data['idex'], 0)
                #self.window_strategy_list.tw_strategy_list.scrollToItem(self.window_strategy_list.tw_strategy_list.currentItem(), QAbstractItemView.PositionAtTop)

                if loaded_data['is_first']:

                    webbrowser.open("https://docs.qq.com/doc/DSUhpcUJoWHF4TExo")
                    self.show_log = ShowLog(
                        "懒人TFT永久免费且已经开源!\n如果你在淘宝闲鱼等商业购买,说明你已经上当了!\n请立即找他们退款!\n请仔细阅读打开的网页中的协议内容,认可则继续,不认可请24小时内删除",
                        time_end=7000, color=(255, 255, 0))
                else:
                    self.show_log = ShowLog("按~反撇号或鼠标侧键_前进 开启/关闭拿牌 \n按Home键 隐藏/显示UI  \n 按 左 右 方向键 光速位移 \n 按End键或鼠标侧键_后退 开启/关闭自动D牌\n\n\n\n懒人TFT永久免费且已经开源!\n如果你在淘宝闲鱼等商业购买,说明你已经上当了!\n请立即找他们退款!",
                                            time_end=10000, color=(255, 255, 0))
                self.show_log.show()

        except Exception as e:
            print(e)
    def save_set(self):
        # 将数据保存到 JSON 文件
        data={}
        data['idex']=self.window_strategy_list.tw_strategy_list.currentIndex().row()
        data['is_first']=False
        data['mode'] = setting.mode
        data['is_side']=self.auto_tft.is_side
        with open('datas/setting.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    def closeEvent(self, event):
        self.save_set()
        qApp.quit()












