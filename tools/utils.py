import ctypes
import json
import math
import sys

import cv2
import numpy as np
import time
from collections import defaultdict
import psutil
import win32api
import win32con
import win32gui
from ctypes import wintypes

from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QGridLayout

import setting 


#单例模式装饰器
def singleton(cls):
    """
    单例模式装饰器
    :param cls: 类
    :return:
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
original_style=0
#这里都是放的一些窗口控制或者进程以及一些杂七杂八的小型便捷函数 懒得归类就都放这里了也方便调用
def window_is_active(hwnd):
    """
    判断给定的窗口句柄是否是当前激活的窗口。

    参数:
        hwnd (int): 窗口句柄

    返回:
        bool: 如果是当前激活窗口，返回 True；否则返回 False。
    """
    # 获取当前处于前台（激活）的窗口句柄
    foreground_hwnd = win32gui.GetForegroundWindow()

    # 比较两个句柄是否相同
    return hwnd == foreground_hwnd
def window_set_mouse_through(hwnd=0, setPenetrate=True):
    '''
    设置窗口鼠标穿透
    :param hwnd: 目标窗口 默认当前窗口
    :param setPenetrate: 是否穿透
    :return:
    '''
    global original_style
    if setPenetrate:
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        original_style = style  # 保存原始样式，以便恢复
        new_style = style | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
    else:
        if original_style == 0:
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
        else:
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, original_style)
def window_set_activate(hwnd=0):
    """
    激活窗口
    :param hwnd: 窗口句柄
    :return:
    """

    try:
        # 判断窗口是否为最小化
        if win32gui.IsIconic(hwnd):
            # 还原窗口
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass
def window_set_display_affinity(hwnd=0):
    '''
    设置窗口 禁止被捕获
    :param hwnd:
    :return:
    '''

    # WDA_NONE
    # 0x00000000
    # 对窗口的显示位置没有限制。
    # WDA_MONITOR
    # 0x00000001
    # 窗口内容仅显示在监视器上。 在其他任何位置，窗口都会显示，其中没有任何内容。
    # WDA_EXCLUDEFROMCAPTURE
    # 0x00000011
    # 窗口仅显示在监视器上。 在其他位置，窗口根本不显示。
    # 此相关性的一个用途是用于显示视频录制控件的窗口，以便控件不包含在捕获中。
    dwAffinity = wintypes.DWORD(0x00000011)  # 使用wintypes模块,“0x00000001”可换成其他值
    dll = ctypes.cdll.LoadLibrary("C:\\WINDOWS\\system32\\user32.dll")  # 接着导入user32.dll 模块
    dll.SetWindowDisplayAffinity(hwnd, dwAffinity)
def window_is_valid(hwnd=0):
    return win32gui.IsWindow(hwnd)

def window_set_show_hide(hwnd=0, show=True):
    '''
    显示隐藏窗口
    :param hwnd:
    :param show:
    :return:
    '''

    if show:
        win32gui.ShowWindow(hwnd, 5)  # 5对应SW_SHOW
    else:
        win32gui.ShowWindow(hwnd, 0)  # 0对应SW_HIDE
def windows_get_screen_scale():
    '''
    获取屏幕缩放比例
    :return:
    '''

    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
        # 计算缩放比例
        scale = round(dpi / 96.0, 2)

        return scale
    except Exception as e:
        print("获取缩放比例时出错:", e)
        return 1
def window_get_handle_at_mouse_position():
    active_hwnd = ctypes.windll.user32.GetForegroundWindow()
    return active_hwnd
def window_set_console_position(x, y, w,h):
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.MoveWindow(hwnd, x, y, w, h, True)
def window_find_child_handle(parent, class_name, window_title):
    hwnd_child = 0
    while True:
        hwnd_child = win32gui.FindWindowEx(parent, hwnd_child, class_name, None)
        if hwnd_child:

            buffer=win32gui.GetWindowText(hwnd_child)
            if window_title in buffer:
                return hwnd_child
        else:
            return 0
def close_process_by_name(process_name):
    '''
    关闭指定名称的进程
    :param process_name:
    :return:
    '''

    # 遍历所有当前运行的进程
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # 检查进程名称
            if proc.info['name'] == process_name:
                # 优雅地终止进程
                proc.terminate()  # 或者使用 proc.kill() 强制结束
                print(f"成功终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
def find_dict_index(dict_list, target_key, target_value, sim_key='confidence'):
    '''
    查找字典列表中，指定键的值匹配目标值，且相似度最高的成员索引

    :param dict_list: 字典列表
    :param target_key: 要匹配的键名
    :param target_value: 要匹配的值
    :param sim_key: 用于比较相似度的键名 (默认'sim')
    :return: 成功返回索引，失败返回-1
    '''
    max_sim = 0
    found_index = -1

    for index, current_dict in enumerate(dict_list):
        # 先检查是否匹配目标键值对
        if current_dict.get(target_key) != target_value:
            continue

        # 获取相似度值，不存在时默认0避免类型错误
        current_sim = current_dict.get(sim_key, 0)

        # 更新最大值和索引
        if current_sim > max_sim:
            max_sim = current_sim
            found_index = index

    return found_index
def count_matching_entries(dict_list, key, value):
    '''
    列表中 字典里指定key 存在某个值的次数
    :param dict_list:
    :param key:
    :param value:
    :return:
    '''
    num_ = 0
    for i, dictionary in enumerate(dict_list):
        if dictionary.get(key) == value:
            num_ += 1
    return num_
def int_to_byte_list(integer_value:int):
    # 转换为字节集（小端顺序）
    byte_array = integer_value.to_bytes(4, byteorder='little')

    return list(byte_array)
def byte_list_to_int(byte_array:list):
    # 将字节集转换为整数（小端顺序）
    integer_value = int.from_bytes(byte_array, byteorder='little')
    return integer_value
def calculate_compass_bearing(from_point, to_point):
    """
    计算从起点到目标点的罗盘方位角（北基准顺时针0-359度）

    :param from_point: 起始点坐标，格式为(x, y)或(longitude, latitude)
    :param to_point: 目标点坐标，格式为(x, y)或(longitude, latitude)
    :return: 整型方位角，范围0-359度
    """
    delta_x = to_point[0] - from_point[0]
    delta_y = to_point[1] - from_point[1]

    radians_angle = math.atan2(delta_y, delta_x)
    degrees_angle = math.degrees(radians_angle)
    compass_angle = int((degrees_angle + 360 + 90) % 360)

    return compass_angle
def calculate_euclidean_distance( point_a ,point_b) -> float:
    """
    计算两点间精确欧氏距离（OpenCV坐标系专用）

    参数说明：
    point_a : 第一个点的(x, y)坐标，支持tuple/list/numpy数组
    point_b : 第二个点的(x, y)坐标

    返回：
    float : 精确距离值（单位与输入坐标一致）

    性能特征：
    - 使用math.hypot优化数值稳定性
    - 支持多种坐标容器类型
    - 类型注解确保IDE自动补全
    """
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    return math.hypot(dx, dy)
def cv2_puttext_chinese(img, text, position, font_size, color_bgr, font_path=r'C:\Windows\Fonts\\msyh.ttc'):

    """
    使用PIL渲染中文文本到OpenCV图像
    参数说明：
    - img: cv2.imread读取的BGR图像
    - text: 要绘制的中文字符串
    - position: (x,y) 文本起始坐标
    - font_size: 字体大小（非像素高度）
    - color_bgr: BGR格式的颜色元组
    - font_path: 中文字体文件路径
    """
    # 转换颜色空间 BGR->RGB
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # 加载字体（建议使用绝对路径）
    font = ImageFont.truetype(font_path, font_size)

    # 绘制文本
    draw.text(position, text, font=font, fill=color_bgr[::-1])  # RGB颜色

    # 转换回OpenCV格式
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
def is_color(rgb_color, target, tolerance=10):
    """
    检查给定的RGB颜色是否在目标颜色的范围内。
    :param rgb_color: 要检查的RGB颜色，格式为 (R, G, B)
    :param target: 目标RGB颜色，格式为 (R, G, B)
    :param tolerance: 容差范围，默认为10
    :return: 如果在范围内，返回True；否则，返回False
    """
    return all(abs(int(c) - int(t)) <= tolerance for c, t in zip(rgb_color, target))
def load_json_file(file_path):
    with open(file_path,'r')as f:
        return  json.load(f)
def save_json_file(file_path,data):
    with open(file_path,'w')as f:
        return  json.dump(data, f)
def CreateNewImage(current_filename, new_filename, new_color):
    '''
    将指定图片转换颜色
    :param current_filename: 图片路径
    :param new_filename: 保存路径
    :param new_color: 转换颜色 []
    :return:
    '''
    image = Image.open(current_filename)

    image_values = np.array(image)

    new_image_values = NewSolidImage(image_values, new_color)
    new_image = Image.fromarray(new_image_values)

    new_image.save(new_filename)
def NewSolidImage(rgba_array, new_color):
    '''
    将图片转换成特定颜色,透明除外!
    :param rgba_array: 图片矩阵 numpy.array(image)获取
    :param new_color: 颜色值 例如:[255,255,255]
    :return: 返回新image
    '''
    new_r, new_g, new_b = new_color
    rows, cols, rgba_size = rgba_array.shape
    if rgba_size != 4:
        raise ValueError('Bad size')

    for row in range(rows):
        for col in range(cols):
            pixel = rgba_array[row][col]
            transparency = pixel[3]
            if transparency != 0:
                new_pixel = pixel.copy()
                new_pixel[0] = new_r
                new_pixel[1] = new_g
                new_pixel[2] = new_b

                rgba_array[row][col] = new_pixel

    return rgba_array
def chessName_get_data(chess, hero_name):
    '''
    根据棋子的name返回棋子数据
    :param chess:
    :param hero_name:
    :return:
    '''
    for item in chess:
        if hero_name == item['displayName']:
            return item
def chessId_get_data(chess, hero_id):
    '''
    根据棋子的id返回棋子数据
    :param chess:
    :param hero_id:
    :return:
    '''

    for item in chess:

        if hero_id == item["chessId"]:

            return item

    raise Exception(f"没有找到这个id chessId={hero_id}")
def equipId_get_data(equip, equip_id):
    '''
    根据装备的id返回装备数据
    :param equip:
    :param equip_id:
    :return:
    '''

    for item in equip:
        if equip_id == item['equipId']:
            return item
    raise Exception(f"没有找到这个id equipId={equip_id}")
def equip_get_dj_Data(equip, xj1, xj2):
    '''
    找到符合合成路线的装备
    :param equip: 装备数据
    :param xj1: 小件1
    :param xj2: 小件2
    :return: 返回找到装备数据
    '''

    for item in equip:
        # 找到合成符合的大件装备
        if item['type'] == '2':
            formula = item['formula'].split(',')

            if xj1 == xj2:
                if xj1 == formula[0] and xj2 == formula[1]:
                    return item
            else:
                if xj1 in formula and xj2 in formula:
                    return item
    raise Exception(f"没有找到这个符合的合成装备 小件1= {xj1} , 小件2= {xj2}")
def jobId_get_data(job, job_id):
    '''
    根据职业的id返回职业数据
    :param job:
    :param job_id:
    :return:
    '''
    for item in job:
        if job_id == item['jobId']:
            return item
    raise Exception(f"没有找到这个id job_id={job_id}")
def raceId_get_data(race, race_id):
    '''
    根据羁绊的id返回羁绊数据
    :param race:
    :param race_id:
    :return:
    '''
    for item in race:
        if race_id == item['raceId']:
            return item
    raise Exception(f"没有找到这个id race_id={race_id}")
def jobName_get_data(job, job_name):
    '''
    根据职业的name返回职业数据
    :param job:
    :param job_name:
    :return:
    '''
    for item in job:
        if job_name == item['name']:
            return item
    raise Exception(f"没有找到这个id job_name={job_name}")
def raceName_get_data(race, race_name):
    '''
    根据羁绊的name返回羁绊数据
    :param race:
    :param race_name:
    :return:
    '''
    for item in race:
        if race_name == item['name']:
            return item
    raise Exception(f"没有找到这个id race_name={race_name}")
def clear_layout(layout):
    """清空布局并删除所有控件"""
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)  # 从布局中取出第一个项
            widget = item.widget()  # 获取该项对应的控件

            if widget is not None:
                # 如果该项是控件，则删除控件
                widget.deleteLater()  # 安全删除控件
            else:
                # 如果该项是子布局，则递归清除
                clear_layout(item.layout())

        # 如果是 QGridLayout，还需要清理 spacer items
        if isinstance(layout, QGridLayout):
            for i in reversed(range(layout.rowCount())):
                for j in reversed(range(layout.columnCount())):
                    item = layout.itemAtPosition(i, j)
                    if item is not None and item.widget() is None:
                        layout.removeItem(item)
def job_get_background_sf(job, job_id, s, sftx=False):
    '''
    返回职业背景图片地址,以及羁绊图标'
    :param job: job数据
    :param job_id: 需要查询的id
    :param s: 羁绊数量
    :param sftx: 是否天选
    :return:返回3个数据 背景图,图标,job数据  返回None表示没达成
    '''
    try:
        itemJob = jobId_get_data(job, job_id)
        level = len(itemJob['level'])
        # 如果有天选
        if sftx == True:
            # 直接返回最华丽的背景图
            return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
        else:
            # 将key取出来
            sss = []
            for item in itemJob['level'].keys():
                sss.append(item)
            if level == 1:  # 只分1个等级时
                return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
            elif level == 2:  # 分2个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]):
                    return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
            elif level == 3:  # 分3个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]):
                    return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
                else:
                    return None

            elif level == 4:  # 分4个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[3]):
                    return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
            elif level == 5:  # 分5个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[3]) and s < int(sss[4]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[4]):
                    return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
            elif level >= 6:  # 分6个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[3]) and s < int(sss[4]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[4]) and s < int(sss[5]):
                    return setting.Path_img + 'bg3.png', setting.Path_job + itemJob['alias'], itemJob
                elif s >= int(sss[5]):
                    return setting.Path_img + 'bg4.png', setting.Path_job2 + itemJob['alias'], itemJob
                else:
                    return None
    except:
        return None
def race_get_background_sf(race, race_id, s, sftx=False):
    '''
    返回羁绊背景图片地址,以及羁绊图标'
    :param race: race数据
    :param race_id: 需要查询的id
    :param s: 羁绊数量
    :param sftx: 是否天选
    :return:返回3个数据 背景图,图标,race数据  返回None表示没达成
    '''
    try:
        itemRace = raceId_get_data(race, race_id)
        level = len(itemRace['level'])
        # 如果有天选
        # 将key取出来
        sss = []
        for item in itemRace['level'].keys():
            sss.append(item)
        if sftx == True:
            # 直接返回最华丽的背景图
            if s >= int(sss[0]):
                return setting.Path_img + 'bg4.png', setting.Path_race2 + itemRace['alias'], itemRace
        else:
            if level == 1:  # 只分1个等级时
                if s >= int(sss[0]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
            elif level == 2:  # 分2个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                else:
                    return None
            elif level == 3:  # 分3个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]):
                    return setting.Path_img + 'bg4.png', setting.Path_race2 + itemRace['alias'], itemRace
                else:
                    return None

            elif level == 4:  # 分4个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[3]):
                    return setting.Path_img + 'bg4.png', setting.Path_race2 + itemRace['alias'], itemRace
                else:
                    return None
            elif level == 5:  # 分5个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[3]) and s < int(sss[4]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[4]):
                    return setting.Path_img + 'bg4.png', setting.Path_race2 + itemRace['alias'], itemRace
                else:
                    return None
            elif level >= 6:  # 分6个阶段时
                if s >= int(sss[0]) and s < int(sss[1]):
                    return setting.Path_img + 'bg2.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[1]) and s < int(sss[2]):
                    return setting.Path_img + 'bg1.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[2]) and s < int(sss[3]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[3]) and s < int(sss[4]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[4]) and s < int(sss[5]):
                    return setting.Path_img + 'bg3.png', setting.Path_race + itemRace['alias'], itemRace
                elif s >= int(sss[5]):
                    return setting.Path_img + 'bg4.png', setting.Path_race2 + itemRace['alias'], itemRace
                else:
                    return None
    except Exception as e:
        print(e)

        return None
def tanChudataForm(chessData, job, race):
    '''
    返回英雄详细资料的text
    :param chessData:
    :param job:
    :param race:
    :return:
    '''
    # ----------------------
    jobtxt = ''
    racetxt = ''
    try:
        for item in chessData['jobIds'].split(','):
            try:
                jobtxt = jobtxt + jobId_get_data(job, item)['name'] + '&nbsp;'
            except:
                pass
    except:
        pass
    try:
        for item in chessData['raceIds'].split(','):
            try:
                racetxt = racetxt + raceId_get_data(race, item)['name'] + '&nbsp;'
            except:
                pass
    except:
        pass
    return f'''
                        <h2 style="color:#FFFFFF;text-align:center;">{chessData['title']}  {chessData['displayName']}</h2>
                        <span style="color:#E7E7E9;">
                        <p style="color:#c6c6c6"><b style="color:#FFFFFF">职业:&nbsp;</b>{jobtxt}</p>
                        <p style="color:#c6c6c6"><b style="color:#FFFFFF">羁绊:&nbsp;</b>{racetxt}</p>
                        <p style="color:#c6c6c6"><b style="color:#FFFFFF">费用:&nbsp;</b>{chessData['price']}</p>
                        <p style="color:#c6c6c6"><b style="color:#FFFFFF">技能:&nbsp;</b>{chessData['skillName']}</p>
                        <p style="color:#c6c6c6">{chessData['skillIntroduce']}</p>
                        </span>
                        '''
def tanChu_EquipData(equip, quipData):
    '''
    返回装备详细资料的text
    :param quipData:
    :return:
    '''
    # ----------------------
    zb_xj = []
    try:
        for item in quipData['formula'].split(','):
            img = setting.Path_equip + equipId_get_data(equip, item)['imagePath'].split('/')[-1]
            zb_xj.append(img)

        return f'''
                            <h2 style="color:#FFFFFF;text-align:center;">{quipData['name']}</h2><br>
                            <img src='{zb_xj[0]}' > 
                            <img src='{zb_xj[1]}' ><b>{quipData['effect']}</b>
                            '''
    except:
        return f'''
                            <h2 style="color:#FFFFFF;text-align:center;">{quipData['name']}</h2><br>
                            <b>{quipData['effect']}</b>
                            '''
def Hero_filter(chess, price='0', jobId='0', raceId='0', keyword=''):
    '''
    根据条件筛选数据 分析chess数据然后绘制列表,注意所有的参数必须为str字符串 '0'表示不考虑这个条件
    :param chess: 字典数据
    :param price: 费用条件
    :param jobId:职业id
    :param raceId:羁绊id
    :param keyword:关键字 搜索
    :return:
    '''
    try:
        tj_list = []  # 条件列表
        # 先判断是否有这个 有的话就加入条件列表
        if price != '0':
            tj_list.append('''x['price'] == price  ''')
        if jobId != '0':
            tj_list.append('''jobId in x['jobIds'].split(',') ''')
        if raceId != '0':
            tj_list.append('''raceId in x['raceIds'].split(',') ''')
        if keyword != '':
            tj_list.append('''keyword in x['displayName'] or keyword in x['title'] ''')
        length = len(tj_list)
        if length == 0:
            return chess
        tj = ''
        # 将需要用到的条件都拼接起来,骚操作
        for i, item in enumerate(tj_list):
            if i == length - 1:  # 最后一个就不加and了
                tj = tj + item
            else:
                tj = tj + item + ' and '

        # 用最强大的方式检索返回符合条件的棋子列表,后面的字典就是给eval中的字符串代码传输变量(非常方便,可以用各种骚操作)
        ls_chess = eval(f'''list(filter(lambda x: {tj}, chess))''',
                        {'chess': chess, 'raceId': raceId, 'jobId': jobId, 'price': price, 'keyword': keyword})

        return ls_chess
    except:

        return chess
def get_max_color(cv_img=None, tolerance=10):
    #只保留3通道
    if cv_img is None:
        return None

    red_region = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2BGR)
    # 颜色统计函数（允许±30色差）
    # 统计颜色
    color_counts = count_colors(red_region,tolerance)
    # 找出出现最多的颜色
    most_common = max(color_counts.items(), key=lambda x: x[1])
    return most_common[0],most_common[1]
def count_colors(region, tolerance=30):
    '''
    统计所有颜色 出现的次数
    :param region:
    :param tolerance:
    :return:
    '''
    color_counts = defaultdict(int)
    for row in region:
        for pixel in row:
            # 将BGR转为元组作为键
            b, g, r = map(int, pixel)
            # 查找相似颜色（已有颜色±30范围内视为相同）
            found = False
            for existing in color_counts:
                if (abs(existing[0] - b) <= tolerance and
                        abs(existing[1] - g) <= tolerance and
                        abs(existing[2] - r) <= tolerance):
                    color_counts[existing] += 1
                    found = True
                    break
            if not found:
                color_counts[(b, g, r)] = 1
    return color_counts
def calculate_color_percentage(cv_img, target_color, tolerance=10):
    """
    计算图像中与目标颜色相近的像素所占百分比（30偏色内都算）

    参数:
        image: numpy数组形式的图像，形状为(height, width, 3)或(height, width, 4)
        target_color: 目标颜色，格式为(R, G, B)或(R, G, B, A)
        tolerance: 颜色容差范围，默认为30

    返回:
        目标颜色占比（0-1之间的浮点数）
    """
    image = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2BGR)
    # 确保图像是numpy数组
    img_array = np.array(image)

    # 提取RGB通道（忽略alpha通道如果存在）
    rgb = img_array[..., :3]

    target_rgb = np.array(target_color[:3])

    # 计算每个像素与目标颜色的欧式距离
    color_diff = np.sqrt(np.sum((rgb - target_rgb) ** 2, axis=2))

    # 统计在容差范围内的像素数量
    matching_pixels = np.sum(color_diff <= tolerance)
    total_pixels = rgb.shape[0] * rgb.shape[1]

    # 计算占比
    percentage = matching_pixels / total_pixels

    return percentage
def is_compiled():
    return (hasattr(sys, 'frozen') or
            hasattr(sys, '_MEIPASS') or
            getattr(sys, 'frozen', False))
def is_button_down(button=1):
    #  0x02  0x01   右键 左键   win32con.VK_LBUTTON
    return win32api.GetAsyncKeyState(button) & 0x8000 != 0
def chess_id_to_tftid(chess_data,chess_id):
    '''
    把tft的chessid转换为tft的id
    :param chess_data:
    :param chess_id:
    :return:
    '''
    for item in chess_data:
        if item['chessId'] == chess_id:
            return item['TFTID']
