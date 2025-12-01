import ctypes
import os
import sys

import win32gui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from decimal import Decimal, ROUND_HALF_UP

def round_lr(num, ndigits=0):
    return int(Decimal(str(num)).quantize(Decimal('1e-{}'.format(ndigits)), rounding=ROUND_HALF_UP))
# 设置DPI感知
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print("注意：无法设置DPI感知，可能导致高分辨率屏幕显示异常。")
# 配置Qt高DPI缩放
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.*=false'
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
Path_chess = 'datas/chess/'
Path_chess_big = 'datas/chess_big/'
Path_equip = 'datas/equip/'
Path_job = 'datas/job/'
Path_race = 'datas/race/'
Path_job2 = 'datas/job2/'
Path_race2 = 'datas/race2/'
Path_img='datas/img/'
Path_img2='datas/img2/'

#判断是否有目录存在 如果不在就创建
if not os.path.exists(Path_chess):os.makedirs(Path_chess)
if not os.path.exists(Path_chess_big):os.makedirs(Path_chess_big)
if not os.path.exists(Path_equip):os.makedirs(Path_equip)
if not os.path.exists(Path_job):os.makedirs(Path_job)
if not os.path.exists(Path_race):os.makedirs(Path_race)
if not os.path.exists(Path_job2):os.makedirs(Path_job2)
if not os.path.exists(Path_race2):os.makedirs(Path_race2)
if not os.path.exists(Path_img):os.makedirs(Path_img)
if not os.path.exists(Path_img2):os.makedirs(Path_img2)
GAME_TITLE="League of Legends (TM) Client"
GAME_CLASS="RiotWindowClass"
HOME_TITLE="League of Legends"
HOME_CLASS="RCLIENT"
# 获取窗口的屏幕坐标（包含边框和标题栏）
hwnd=win32gui.FindWindow(GAME_CLASS, GAME_TITLE)
if hwnd!=0:
    rect = win32gui.GetWindowRect(hwnd)
    # 获取客户区尺寸（这里的left/top始终为0，right/bottom是客户区宽高）
    client_rect = win32gui.GetClientRect(hwnd)
    # 将客户区左上角坐标转换为屏幕坐标
    pt_origin = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
    # 将客户区右下角坐标转换为屏幕坐标
    pt_end = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))
    # 计算实际物理尺寸
    window_width = pt_end[0] - pt_origin[0]
    window_height = pt_end[1] - pt_origin[1]
    # 直接使用转换后的客户区坐标
    p_left = pt_origin[0]
    p_top = pt_origin[1]
else:
    # 获取显示器物理分辨率
    hdc = ctypes.windll.user32.GetDC(0)
    window_width = ctypes.windll.gdi32.GetDeviceCaps(hdc, 118)  # HORZRES
    window_height = ctypes.windll.gdi32.GetDeviceCaps(hdc, 117)  # VERTRES
    ctypes.windll.user32.ReleaseDC(0, hdc)
    p_left = 0
    p_top = 0
ratio =window_width / 2560  # 比例
if ratio<0.1:
    # 获取显示器物理分辨率
    hdc = ctypes.windll.user32.GetDC(0)
    window_width = ctypes.windll.gdi32.GetDeviceCaps(hdc, 118)  # HORZRES
    window_height = ctypes.windll.gdi32.GetDeviceCaps(hdc, 117)  # VERTRES
    ctypes.windll.user32.ReleaseDC(0, hdc)
    ratio = window_width / 2560  # 比例
    p_left = 0
    p_top = 0
#prround_lr(window_width)
# 计算字体大小
base_font_size = 13
# 基准字体大小，适合2560*1440分辨率
new_font_size = round_lr(base_font_size * ratio)
font = QFont("Arial", new_font_size)
prod_gold={"x":round_lr(857*ratio),"y":round_lr(1404*ratio),"color":[210,184,126]}

# 小队提醒的位置
prod_area_steps=[round_lr(267*ratio),round_lr(269*ratio),round_lr(269*ratio),round_lr(269*ratio)]

prod_color=[13,19,22] #没有推荐棋子时的颜色  RGB
#挑选的几个位置颜色是否有变化来判断是否出现提醒
prod_x1=round_lr(658*ratio)
prod_x2=round_lr(663*ratio)
prod_x3=round_lr(673*ratio)
prod_x4=round_lr(677*ratio)
prod_x5=round_lr(686*ratio)
prod_y=round_lr(1235*ratio)
#5个商品位置的判断坐标合集
prod_area_list=[]
for prod_area in range(5):
    prod_area_list.append([{"x":prod_x1 +sum(prod_area_steps[:prod_area]) , "y":prod_y},
                           {"x": prod_x2 +sum(prod_area_steps[:prod_area]), "y": prod_y},
                           {"x": prod_x3 +sum(prod_area_steps[:prod_area]), "y": prod_y},
                           {"x": prod_x4 +sum(prod_area_steps[:prod_area]), "y": prod_y},
                           {"x": prod_x5 +sum(prod_area_steps[:prod_area]), "y": prod_y},
                           ])


#扎克组织细胞1072
prod_zack_list=[
{"x":round_lr(877*ratio),"y":round_lr(1398*ratio),"color":[230,230,230]}, #最上面
{"x":round_lr(881*ratio),"y":round_lr(1405*ratio),"color":[230,230,230]},#左边
{"x":round_lr(873*ratio),"y":round_lr(1405*ratio),"color":[230,230,230]},#右边
{"x":round_lr(878*ratio),"y":round_lr(1413*ratio),"color":[230,230,230]},#下边
{"x":round_lr(877*ratio),"y":round_lr(1405*ratio),"color":[79,108,107]}#中间
]



#边框默认颜色  来判断现在是否是购买棋子界面
prod_box_color=[148,122,66] #没有推荐棋子时的颜色  RGB
prod_box_pos_list=[
{"x": round_lr(884*ratio), "y": round_lr(1222*ratio)},
{"x": round_lr(747*ratio), "y": round_lr(1222*ratio)},
{"x": round_lr(1047*ratio), "y": round_lr(1222*ratio)},
{"x": round_lr(1310*ratio), "y": round_lr(1222*ratio)},
{"x": round_lr(1570*ratio), "y": round_lr(1222*ratio)},
{"x": round_lr(1812*ratio), "y": round_lr(1222*ratio)},
]
prod_click_x=round_lr(777*ratio)  #第一个商品点击的x
prod_click_y=round_lr(1328*ratio) #第一个商品点击的y
prod_click_pos_list=[]
for i in range(5):
    prod_click_pos_list.append({"x":prod_click_x +sum(prod_area_steps[:i]), "y":prod_click_y})
#这坐标 用来粘贴小队的
xiaodui_bt_pos=[
    {"x":round_lr(2152*ratio),"y":round_lr(32*ratio)},
    {"x": round_lr(494 * ratio), "y": round_lr(112 * ratio)},
    # {"x": round_lr(2063 * ratio), "y": round_lr(399 * ratio)},
    # {"x": round_lr(1856 * ratio), "y": round_lr(433 * ratio)},
    #{"x": round_lr(1118 * ratio), "y": round_lr(655 * ratio)},
    {"x": round_lr(1472*ratio), "y": round_lr(254*ratio)},
    {"x": round_lr(1697*ratio), "y": round_lr(815*ratio)},
    {"x": round_lr(2148 * ratio), "y": round_lr(148 * ratio)},
]

#判断是否是天选  如果是天选 不帮忙买防止错乱,,

color_god=[16,34,35]
pos_god=[round_lr(1977*ratio),round_lr(1255*ratio)]


#光速位移  需要交换的坐标  最左右 2个格子
location_pos_list=[

    # 第四行
    {"x1": round_lr(781 * ratio), "y1": round_lr(850 * ratio), "x2": round_lr(1812 * ratio), "y2": round_lr(850 * ratio)},
    {"x1": round_lr((948) * ratio), "y1": round_lr(869* ratio), "x2": round_lr(1613 * ratio), "y2": round_lr(862 * ratio)},
    #{"x1": round_lr((781 + 171+171) * ratio), "y1": round_lr(906 * ratio), "x2": round_lr((1812 - 171-171) * ratio), "y2": round_lr(906 * ratio)},

    # 第三行
    {"x1": round_lr(697 * ratio), "y1": round_lr(760 * ratio), "x2": round_lr(1703 * ratio), "y2": round_lr(790 * ratio)},
    {"x1": round_lr((697 + 167) * ratio), "y1": round_lr(774 * ratio), "x2": round_lr((1703 - 167) * ratio), "y2": round_lr(774 * ratio)},
    #{"x1": round_lr((697 + 167+ 167) * ratio), "y1": round_lr(774 * ratio), "x2": round_lr((1703 - 167-167) * ratio), "y2": round_lr(774 * ratio)},


    # 第一行
    {"x1": round_lr(751 * ratio), "y1": round_lr(580 * ratio), "x2": round_lr(1674 * ratio), "y2": round_lr(580 * ratio)},
    {"x1": round_lr((751 + 154) * ratio), "y1": round_lr(580 * ratio), "x2": round_lr((1674 - 154) * ratio), "y2": round_lr(580 * ratio)},
    #{"x1": round_lr((751 + 154+ 154) * ratio), "y1": round_lr(580 * ratio), "x2": round_lr((1674 - 154- 154) * ratio), "y2": round_lr(580 * ratio)},

    # 第二行
    {"x1": round_lr(813 * ratio), "y1": round_lr(685 * ratio), "x2": round_lr(1761 * ratio), "y2": round_lr(685 * ratio)},
    {"x1": round_lr((813 + 158) * ratio), "y1": round_lr(685 * ratio), "x2": round_lr((1761 - 158) * ratio), "y2": round_lr(685 * ratio)},
    #{"x1": round_lr((813 + 158+ 158) * ratio), "y1": round_lr(685 * ratio), "x2": round_lr((1761 - 158-158) * ratio), "y2": round_lr(685 * ratio)},

]

mode=1 #赛博之城  2 强音争霸
ver="1.34"
mode_mn=2 #  1 5是外服
side=True #是否启用侧键
video_url="https://www.bilibili.com/video/BV1Jc411i7Qj/"
author_url="https://space.bilibili.com/394281846"
author_url="https://space.bilibili.com/394281846"
sponsorship_url="http://w.kami.vip/s/FSUtd45z"

chess_url= "http://game.gtimg.cn/images/lol/act/img/tft/champions/"
chess_big_url="http://game.gtimg.cn/images/lol/tftstore/s12/624x318/"

# 添加临时路径
temp_path = os.path.dirname(__file__) + "\\"
sys.path.append(temp_path)
# 获取当前的PATH环境变量
original_path = os.environ['PATH']
os.environ['PATH'] = temp_path + os.pathsep + original_path