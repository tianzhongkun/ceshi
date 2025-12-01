import importlib
import threading
import time
import traceback

import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

from moni.hook_key_mouse import HookKeyMouse
from moni.moni import MoNiInterface,MoNi
from tools.utils import is_color, window_set_activate, get_max_color, calculate_color_percentage, is_button_down, \
    window_is_valid, window_is_active
from tools.screenshot import screenshot
import setting
class AutoTFT(HookKeyMouse):
    def __init__(self, moni: MoNiInterface):
        super().__init__(hookKey=True, hookMouse=True)
        self.is_runing=False
        self.is_pause=False
        self.is_change_location=False
        self.num_err = 0
        self.moni=moni
        self.screen=None
        self.sg=None
        self.is_auto_start=False
        self.is_auto_ddd=False
        self.is_side=True
        self.max_color=None
    def set_sg(self,sg):
        self.sg=sg
    def on_release(self, key):

        if key == KeyCode.from_char('`'):
            self.change_auto_runing_statu()
        elif key == Key.end:
            self.change_auto_ddd_status()
        elif key == Key.home:
            self.sg.hide_ui.emit()
        elif key == Key.up:
            #取到当前窗口句柄
            hwnd = win32gui.GetForegroundWindow()
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
            if hwnd==self.moni.hwnd:
                self.sg.switch_id.emit(False)
        elif key == Key.down:
            hwnd = win32gui.GetForegroundWindow()
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
            if hwnd == self.moni.hwnd:
                self.sg.switch_id.emit(True)
        elif key == Key.left:
            hwnd = win32gui.GetForegroundWindow()
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
            if hwnd == self.moni.hwnd:
                self.sg.show_log.emit("光速位移\n←←←←←←←←←", (255, 255, 0), 600)
                threading.Thread(target=self.run_change_location,args=(2,),daemon=True).start()
        elif key == Key.right:
            hwnd = win32gui.GetForegroundWindow()
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
            if hwnd == self.moni.hwnd:
                self.sg.show_log.emit("光速位移\n→→→→→→→→→", (255, 255, 0), 600)
                threading.Thread(target=self.run_change_location,args=(1,),daemon=True).start()

    def on_click(self, x, y, button, pressed):
        if self.is_side:
            if button ==Button.x2 and not pressed:
                self.change_auto_runing_statu()
            elif button == Button.x1 and not pressed:
                self.change_auto_ddd_status()

    def bind(self,hwnd):
            self.moni.bind(hwnd)
    def change_auto_ddd_status(self):
        if self.is_auto_ddd:
            self.sg.show_log.emit("结束自动D牌", (255, 0, 0), 2000)
            self.is_auto_ddd = False
        else:
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
                return
            self.sg.show_log.emit("正在自动D牌 再次按下鼠标侧键_后退 关闭", (255, 255, 0), 2000 * 1000)
            self.is_auto_ddd = True
            if not self.is_runing:
                self.is_runing = True
                threading.Thread(target=self.run, daemon=True).start()
    def change_auto_runing_statu(self):
        if self.is_runing:
            self.sg.show_log.emit("关闭拿牌模式", (255, 0, 0), 2000)
            self.is_runing = False
            self.is_auto_ddd = False
        else:
            if not window_is_valid(self.moni.hwnd):
                self.get_game_hwnd()
            self.sg.show_log.emit("开启拿牌模式 \n商店中遇到2星或3星也会自动购买\n可以小队规划器自己增减棋子", (255, 255, 0), 4000)
            self.is_runing = True
            threading.Thread(target=self.run, daemon=True).start()
    def should_click(self):
        '''
        判断是否应该点击
        :return: 返回 -1 -2 -3 -4  代表没有找到  0代表第一个 1代表第二个 以此类推
        '''
        self.screen=self.get_screen()
        if is_button_down(1):
            return -1
        if self.screen is None or self.moni.hwnd==0:
            return -3
        try:

            is_ok=True
            #先判断当前是否为购买棋子的界面
            for p in setting.prod_box_pos_list:
                color_bgr = self.screen[p['y'], p['x']]
                color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
                #print(p['x'],p['y'],color_rgb,setting.prod_box_color)
                if not is_color(color_rgb, setting.prod_box_color, tolerance=40):
                    is_ok=False
            if not is_ok:
                return -2
            # 判断是否是扎克组织细胞
            # if setting.mode == 1 :
            #     for i in range(5):
            #         is_ok = True
            #         for prod_zack in setting.prod_zack_list:
            #             x = prod_zack['x'] + sum(setting.prod_area_steps[:i])
            #             y = prod_zack['y']
            #             color_bgr = self.screen[y, x]
            #             color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
            #             # print(i ,x, y,color_rgb,prod_zack["color"])
            #             if not is_color(color_rgb, prod_zack["color"], tolerance=50):
            #                 # 只要有一个颜色不对 就不是
            #                 is_ok = False
            #                 break
            #         if is_ok:
            #             return i

            #判断商品区域哪个是推荐的
            ret_err=-1
            for i,prod_area in enumerate( setting.prod_area_list):
                for p in prod_area:
                    color_bgr = self.screen[p['y'], p['x']]
                    color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]

                    if not is_color(color_rgb,setting.prod_color,tolerance=20):
                        #判断是否买得起
                        color_bgr = self.screen[setting.prod_gold['y'], setting.prod_gold['x']+sum(setting.prod_area_steps[:i])]
                        color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]

                        #print(setting.prod_gold['y'], setting.prod_gold['x']+ setting.prod_area_step * i,color_rgb,setting.prod_gold["color"])
                        if is_color(color_rgb, setting.prod_gold["color"], tolerance=50):

                            if setting.mode == 2 and i == 4:  # 天选格子
                                color_god_bgr = self.screen[setting.pos_god[1], setting.pos_god[0]]
                                color_god_rgb = [color_god_bgr[2], color_god_bgr[1], color_god_bgr[0]]
                                if not is_color(color_god_rgb, setting.color_god, tolerance=30):
                                    return -1

                            return i
                        else:
                            if self.is_auto_ddd:
                                self.sg.show_log.emit("结束自动D牌", (255, 0, 0), 2000)
                                self.is_auto_ddd = False
                        ret_err=-99
            return ret_err
        except:
            print(traceback.format_exc())

            return -3
    def get_screen(self):
        return screenshot(self.moni.hwnd, 0, 0, self.moni.window_width, self.moni.window_height)
    def click_prod(self,index=0):
        '''
        点击商品
        :param index: 商品的索引 0代表第一个 1代表第二个 以此类推
        :return:
        '''

        if index<0 or index>=5 :
            print(index)
            return False
        window_set_activate(self.moni.hwnd)
        self.moni.mouse_move(setting.prod_click_pos_list[index]['x'],setting.prod_click_pos_list[index]['y'])
        time.sleep(0.01)
        if is_button_down(1):
            return True
        self.moni.mouse_left_down(setting.prod_click_pos_list[index]['x'],setting.prod_click_pos_list[index]['y'])
        time.sleep(0.03)
        self.moni.mouse_left_up(setting.prod_click_pos_list[index]['x'],setting.prod_click_pos_list[index]['y'])
        time.sleep(0.2)
        #判断是否购买成功prod_color
        self.screen = self.get_screen()
        for p in setting.prod_area_list[index]:
            color_bgr = self.screen[p['y'], p['x']]
            color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
            #print(p['x'],p['y'],color_rgb,setting.prod_color)
            #如果发现有一个颜色不一样  说明没有买成功还是属于提醒状态
            if not is_color(color_rgb, setting.prod_color, tolerance=40):
                return False
        return  True
    def click_confirmed(self):
        hwnd = win32gui.FindWindow(setting.GAME_CLASS, setting.GAME_TITLE)
        if hwnd==0:
            return
        self.sg.hide_ui.emit()
        for i,pos in enumerate(setting.xiaodui_bt_pos):
            time.sleep(0.2)
            self.moni.mouse_move(pos['x'], pos['y'])
            time.sleep(0.04)
            if not window_is_active(hwnd):
                self.moni.mouse_left_down(pos['x'], pos['y'])
                time.sleep(0.02)
                self.moni.mouse_left_up(pos['x'], pos['y'])
                time.sleep(0.1)
                self.moni.mouse_left_down(pos['x'], pos['y'])
                time.sleep(0.02)
                self.moni.mouse_left_up(pos['x'], pos['y'])
            else:
                self.moni.mouse_left_down(pos['x'], pos['y'])
                time.sleep(0.02)
                self.moni.mouse_left_up(pos['x'], pos['y'])
        self.sg.hide_ui.emit()
    def get_game_hwnd(self):
        hwnd=win32gui.FindWindow(setting.GAME_CLASS, setting.GAME_TITLE)
        if hwnd!=0:
            mode=setting.mode
            importlib.reload(setting)  # 强制重新加载
            setting.mode=mode
            if setting.window_width>=640:
                self.bind(hwnd)
                self.max_color = None
                return hwnd
            else:
                return 0
        return 0
    def run(self):
        self.num_err=0
        self.is_runing=True
        index_2_count=0
        while True:
            if not self.is_runing:
                return
            if self.is_change_location:
                time.sleep(0.5)
                continue
            try:
                index = self.should_click()
                if index >= 0 :
                    index_2_count=0
                    _ret=self.click_prod(index)
                    if _ret:
                        self.num_err=0

                    else:
                        self.num_err+=1
                        if self.num_err>=2:
                            self.is_runing = False
                            self.is_auto_ddd=False
                            self.sg.show_log.emit("提醒:目前已关闭自动拿牌 按~键恢复", (255, 0, 0),10000)
                            return
                        else:
                            time.sleep(0.3)
                elif index ==-3:
                    time.sleep(2)
                    self.get_game_hwnd()
                    if self.is_auto_ddd:
                        self.is_auto_ddd = False
                        self.sg.show_log.emit("对局已经关闭!", (255, 0, 0),2000)
                        return
                else:
                    index_2_count+=1
                    time.sleep(0.1)
                    if self.is_auto_ddd and index_2_count>=1 and index!=-99:
                        if window_is_active(self.moni.hwnd) and not is_button_down(1):
                            self.moni.key_press("d")
                            time.sleep(0.2)

            except :
                print(traceback.format_exc())
                time.sleep(2)
                self.get_game_hwnd()
    def run_change_location(self,fx=1):
        if self.is_change_location:
            return
        self.is_change_location=True
        for pos in setting.location_pos_list:

            if fx==1:
                self.moni.mouse_left_down(pos['x1'], pos['y1'])
                time.sleep(0.03)
                self.moni.mouse_move(pos['x2'], pos['y2'])
                time.sleep(0.03)
                self.moni.mouse_left_up(pos['x2'], pos['y2'])
            elif fx==2:
                self.moni.mouse_left_down(pos['x2'], pos['y2'])
                time.sleep(0.03)
                self.moni.mouse_move(pos['x1'], pos['y1'])
                time.sleep(0.03)
                self.moni.mouse_left_up(pos['x1'], pos['y1'])
            time.sleep(0.03)

        self.is_change_location = False
    def run_auto_start(self):
        mn=MoNi().create(0,setting.mode_mn)
        while True:
            hwnd = win32gui.FindWindow(setting.GAME_CLASS, setting.GAME_TITLE)
            if hwnd != 0:
                time.sleep(1)
                continue
            if not self.is_auto_start:
                time.sleep(1)
                continue
            hwnd_home=win32gui.FindWindow(setting.HOME_CLASS, setting.HOME_TITLE)
            if hwnd_home==0:
                time.sleep(1)
                continue
            mn.bind(hwnd_home)

            screen=screenshot(hwnd_home, 0, 0, mn.window_width, mn.window_height)
            if screen is None:
                time.sleep(1)
                continue
            ratio = mn.window_width / 1600  # 比例
            home_color1 =[1,10,19]
            home_color2 = [75,63,41]
            home_color3 = [10,195,182]
            home_color4=[178,236,243]
            point_home_click_x= setting.round_lr(786 * ratio)
            point_home_click_y= setting.round_lr(696 * ratio)
            point_home_target_x1= setting.round_lr(1434 * ratio)
            point_home_target_y1= setting.round_lr(12 * ratio)
            point_home_target_x2 = setting.round_lr(1576 * ratio)
            point_home_target_y2 = setting.round_lr(121 * ratio)
            point_home_target_x3 = setting.round_lr(698 * ratio)
            point_home_target_y3 = setting.round_lr(668 * ratio)
            color_bgr = screen[point_home_target_y1, point_home_target_x1]
            color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
            #print(1,home_color1,color_rgb)
            #是否为半遮挡的情况
            if not is_color(color_rgb, home_color1, tolerance=5):
                color_bgr = screen[point_home_target_y2, point_home_target_x2]
                color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
                #print(2, home_color2,color_rgb)
                #并且此时有那个对局匹配好了的x
                if is_color(color_rgb, home_color2, tolerance=10):
                    #并且 此时中间是橙色的
                    color_bgr = screen[point_home_target_y3, point_home_target_x3]
                    color_rgb = [color_bgr[2], color_bgr[1], color_bgr[0]]
                    if is_color(color_rgb, home_color3, tolerance=15) or is_color(color_rgb, home_color4, tolerance=15):

                        if self.is_auto_start and not is_button_down(1):
                            #点击接受按钮
                            #激活
                            window_set_activate(hwnd_home)
                            mn.mouse_left_click(point_home_click_x,point_home_click_y)
                            time.sleep(1)
                            mn.mouse_left_click(point_home_click_x, point_home_click_y)
                            time.sleep(3)

            time.sleep(1)

if __name__ == '__main__':
    moni =MoNi().create( 2559938,2)
    auto_tft=AutoTFT(moni)
    auto_tft.get_game_hwnd(2559938)
    # 启动全局钩子
    HookKeyMouse.start_global_hook()
    auto_tft.run()

    while True:
        time.sleep(1)










