# -*- coding: utf-8 -*-
import time
from abc import ABC, abstractmethod
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
from moni import pydirectinput
from tools.utils import byte_list_to_int

VK_CODE = {
    # 基础键位
    'left_mouse': 0x01, 'right_mouse': 0x02, 'cancel': 0x03,
    'middle_mouse': 0x04, 'x1_mouse': 0x05, 'x2_mouse': 0x06,

    # 控制键
    'backspace': 0x08, 'tab': 0x09,
    'clear': 0x0C, 'enter': 0x0D, 'shift': 0x10,
    'ctrl': 0x11, 'alt': 0x12, 'pause': 0x13,
    'caps_lock': 0x14, 'esc': 0x1B, 'space': 0x20,
    'page_up': 0x21, 'page_down': 0x22, 'end': 0x23,
    'home': 0x24, 'left': 0x25, 'up': 0x26,
    'right': 0x27, 'down': 0x28, 'select': 0x29,
    'print': 0x2A, 'execute': 0x2B, 'print_screen': 0x2C,
    'insert': 0x2D, 'delete': 0x2E, 'help': 0x2F,  'win':0x5B,

    # 数字键
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,

    # 字母键
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
    'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
    'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
    'z': 0x5A,

    # 系统键
    'left_win': 0x5B, 'right_win': 0x5C, 'apps': 0x5D,
    'sleep': 0x5F,

    # 小键盘
    'num_0': 0x60, 'num_1': 0x61, 'num_2': 0x62,
    'num_3': 0x63, 'num_4': 0x64, 'num_5': 0x65,
    'num_6': 0x66, 'num_7': 0x67, 'num_8': 0x68,
    'num_9': 0x69,
    'num_multiply': 0x6A, 'num_add': 0x6B, 'num_separator': 0x6C,
    'num_subtract': 0x6D, 'num_decimal': 0x6E, 'num_divide': 0x6F,

    # 功能键
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73,
    'f5': 0x74, 'f6': 0x75, 'f7': 0x76, 'f8': 0x77,
    'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B,
    'f13': 0x7C, 'f14': 0x7D, 'f15': 0x7E, 'f16': 0x7F,
    'f17': 0x80, 'f18': 0x81, 'f19': 0x82, 'f20': 0x83,
    'f21': 0x84, 'f22': 0x85, 'f23': 0x86, 'f24': 0x87,

    # 状态键
    'num_lock': 0x90, 'scroll_lock': 0x91,

    # 组合修饰键
    'left_shift': 0xA0, 'right_shift': 0xA1,
    'left_ctrl': 0xA2, 'right_ctrl': 0xA3,
    'left_alt': 0xA4, 'right_alt': 0xA5,


    # 多媒体键（需要新版本系统）
    'browser_back': 0xA6, 'browser_forward': 0xA7,
    'browser_refresh': 0xA8, 'browser_stop': 0xA9,
    'browser_search': 0xAA, 'browser_favorites': 0xAB,
    'browser_home': 0xAC, 'volume_mute': 0xAD,
    'volume_down': 0xAE, 'volume_up': 0xAF,
    'media_next': 0xB0, 'media_prev': 0xB1,
    'media_stop': 0xB2, 'media_play_pause': 0xB3,
    'launch_mail': 0xB4, 'launch_media_select': 0xB5,
    'launch_app1': 0xB6, 'launch_app2': 0xB7,

    # 特殊符号
    ';': 0xBA, '=': 0xBB, ',': 0xBC,
    '-': 0xBD, '.': 0xBE, '/': 0xBF,
    '`': 0xC0, '[': 0xDB, '\\': 0xDC,
    ']': 0xDD, "'": 0xDE,

    # 语言相关
    'oem_8': 0xDF, 'oem_102': 0xE2,

    # IME 键
    'ime_process': 0xE5, 'ime_accept': 0xE6, 'ime_convert': 0x1C,
    'ime_nonconvert': 0x1D, 'ime_kana': 0x15, 'ime_hanja': 0x19,

    # 其他
    'attn': 0xF6, 'crsel': 0xF7, 'exsel': 0xF8,
    'erase_eof': 0xF9, 'play': 0xFA, 'zoom': 0xFB,
    'pa1': 0xFD, 'oem_clear': 0xFE
}
# 别名扩展（兼容不同名称）
VK_CODE.update({
    'escape': VK_CODE['esc'],
    'return': VK_CODE['enter'],
    'control': VK_CODE['ctrl'],
    'windows': VK_CODE['left_win'],
    'menu': VK_CODE['alt'],
    'shift_l': VK_CODE['left_shift'],
    'shift_r': VK_CODE['right_shift'],
    'ctrl_l': VK_CODE['left_ctrl'],
    'ctrl_r': VK_CODE['right_ctrl'],
    'alt_l': VK_CODE['left_alt'],
    'alt_r': VK_CODE['right_alt']
})
# 定义MOUSEINPUT结构体
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
# 定义KEYBDINPUT结构体
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.wintypes.WORD),
                ("wScan", ctypes.wintypes.WORD),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
# 定义INPUT结构体
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT),
                    ("ki", KEYBDINPUT)]

    _fields_ = [("type", ctypes.c_ulong),
                ("input", _INPUT)]
# 模拟键鼠接口
class MoNiInterface(ABC):
    def __init__(self, hwnd=0):

        self.original_style = 0
        self.hwnd = hwnd
        self.p_left = 0
        self.p_top = 0
        self.window_width = 0
        self.window_height = 0
        self.window_border_width = 0  # 左边框宽度
        self.window_title_bar_height = 0  # 标题栏高度
        self.window_bottom_border = 0  # 下边框高度
        # 获取当前屏幕宽度和高度
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.send = ctypes.windll.user32.SendInput
        self.down_key_list=[]
        self.down_mouse_list = []

    @abstractmethod
    def bind(self, hwnd):
        pass

    def unbind(self):
        self.hwnd = 0
        self.p_left = 0
        self.p_top = 0
        self.window_width = 0
        self.window_height = 0

    @abstractmethod
    def mouse_move(self):
        pass

    @abstractmethod
    def mouse_mover(self):
        pass

    @abstractmethod
    def mouse_wheel(self):
        pass

    @abstractmethod
    def mouse_middle_down(self):
        pass

    @abstractmethod
    def mouse_middle_up(self):
        pass

    @abstractmethod
    def mouse_left_down(self):
        pass

    @abstractmethod
    def mouse_left_up(self):
        pass

    @abstractmethod
    def mouse_right_down(self):
        pass

    @abstractmethod
    def mouse_right_up(self):
        pass

    @abstractmethod
    def mouse_left_click(self):
        pass

    @abstractmethod
    def mouse_right_click(self):
        pass

    @abstractmethod
    def mouse_middle_click(self):
        pass
    @abstractmethod
    def key_down(self,vk_code):
        pass

    @abstractmethod
    def key_up(self,vk_code):
        pass

    @abstractmethod
    def key_press(self):
        pass

    def up_all(self):
        """
        释放所有的按键
        :return: 
        """
        for vk_code in self.down_key_list:
            self.key_up(vk_code)

        for key in self.down_mouse_list:
            if key=="left":
                self.mouse_left_up()
            elif key=="right":
                self.mouse_right_up()
            else:
                self.mouse_middle_up()
        self.down_key_list=[]
        self.down_mouse_list = []
    def _add_key_down_list(self,key):
        if key not in self.down_key_list:
            self.down_key_list.append(key)
    def _remove_key_down_list(self,key):
        try:
            self.down_key_list.remove(key)
        except:
            pass
    def _add_mouse_down_list(self,key):
        if key not in self.down_mouse_list:
            self.down_mouse_list.append(key)
    def _remove_mouse_down_list(self,key):
        try:
            self.down_mouse_list.remove(key)
        except:
            pass
    # 后台键鼠实现
class MoNiBackstage(MoNiInterface):
    def __init__(self, hwnd=0,mode="post"):
        super().__init__(hwnd)
        self.hwnd = hwnd
        self.bind(self.hwnd)
        self.mode = mode
        # 获取当前屏幕宽度和高度
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.send = ctypes.windll.user32.SendInput
        self.old_x = 0
        self.old_y = 0
    def bind(self, hwnd):
        self.hwnd = hwnd
        if self.hwnd != 0:
            # 获取客户区尺寸（这里的left/top始终为0，right/bottom是客户区宽高）
            client_rect = win32gui.GetClientRect(hwnd)

            # 将客户区左上角坐标转换为屏幕坐标
            pt_origin = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))

            # 将客户区右下角坐标转换为屏幕坐标
            pt_end = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))

            # 计算实际物理尺寸
            self.window_width = pt_end[0] - pt_origin[0]
            self.window_height = pt_end[1] - pt_origin[1]

            self.window_border_width = 0  # 左边框宽度
            self.window_title_bar_height = 0  # 标题栏高度
            self.window_bottom_border = 0  # 下边框高度
            self.p_left = 0
            self.p_top = 0
        else:
            self.window_width = 0
            self.window_height = 0
            self.window_border_width = 0  # 左边框宽度
            self.window_title_bar_height = 0  # 标题栏高度
            self.window_bottom_border = 0  # 下边框高度
            self.p_left = 0
            self.p_top = 0
    def mouse_middle_down(self, x=None, y=None,hwnd=0):
        self.activate(hwnd)
        if hwnd == 0:
            hwnd=self.hwnd
        self._add_mouse_down_list("middle")
        if x is None or y is None:
            win32gui.PostMessage(
                hwnd, win32con.WM_MBUTTONDOWN, win32con.MK_MBUTTON, 0
            )  # 鼠标中键按下
        else:
            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)  # 生成坐标
            win32gui.PostMessage(
                hwnd, win32con.WM_MBUTTONDOWN, win32con.MK_MBUTTON, long_position
            )  # 鼠标中键按下
    def mouse_middle_up(self, x=None, y=None,hwnd=0):
        self._remove_mouse_down_list("middle")
        if hwnd == 0:
            hwnd = self.hwnd
        if x is None or y is None:
            win32gui.PostMessage(
                hwnd, win32con.WM_MBUTTONUP, win32con.MK_MBUTTON, 0
            )  # 鼠标中键抬起
        else:
            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)  # 生成坐标
            win32gui.PostMessage(
                hwnd, win32con.WM_MBUTTONUP, win32con.MK_MBUTTON, long_position
            )  # 鼠标中键抬起
    def mouse_left_down(self,  x=None, y=None,hwnd=0):
        self.activate(hwnd)
        self._add_mouse_down_list("left")
        if hwnd == 0:
            hwnd=self.hwnd
        if x is None or y is None:
            long_position =0

        else:
            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)
        if self.mode == "post":

            win32gui.PostMessage(
                hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position
            )
        else:
            win32gui.SendMessage(
                hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position
            )
    def mouse_left_up(self, x=None, y=None,hwnd=0):
        self._remove_mouse_down_list("left")
        if hwnd == 0:
            hwnd = self.hwnd
        if x is None or y is None:
            long_position = 0
        else:
            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)
        if self.mode == "post":
            win32gui.PostMessage(
                hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position
            )
        else:
            win32gui.SendMessage(
                hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position
            )
    def mouse_right_down(self, x=None, y=None,hwnd=0):
        self.activate(hwnd)
        self._add_mouse_down_list("right")
        if hwnd == 0:
            hwnd = self.hwnd
        if x is None or y is None:
            win32gui.PostMessage(
                hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, 0
            )
        else:

            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)
            win32gui.PostMessage(
                hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position
            )
    def mouse_right_up(self, x=None, y=None,hwnd=0):
        self._remove_mouse_down_list("right")
        if hwnd == 0:
            hwnd = self.hwnd
        if x is None or y is None:
            win32gui.PostMessage(
                hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, 0
            )
        else:

            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            long_position = win32api.MAKELONG(x, y)
            win32gui.PostMessage(
                hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position
            )
    def mouse_wheel(self, count= 120,x=None, y=None,hwnd=0):
        self.activate(hwnd)
        if hwnd == 0:
            hwnd = self.hwnd
        if x is None or y is None:
            lParam = 0
        else:
            x = x if isinstance(x, int) else int(x)
            y = y if isinstance(y, int) else int(y)
            lParam = win32api.MAKELONG(x, y)
        count = count if isinstance(count, int) else int(count)
        wParam = win32api.MAKELONG(0, win32con.WHEEL_DELTA * count)
        win32gui.SendMessage(hwnd, win32con.WM_MOUSEWHEEL, wParam, lParam)
    def key_down(self, vk_code=0,is_activeate=True,hwnd=0):
        try:
            self._add_key_down_list(vk_code)
            if hwnd == 0:
                hwnd = self.hwnd
            #logger.info(f"按下 {key}")
            if is_activeate:
                self.activate(self)
            if isinstance(vk_code, str):
                vk_code= VK_CODE[vk_code.lower()]
            scan_code=ctypes.windll.user32.MapVirtualKeyA(vk_code, 0)
            lParam = byte_list_to_int([1,0,scan_code,32])
            if self.mode == "post":
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam)
            else:
                win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam)


        except:
            pass
    def key_up(self, vk_code=0,is_activeate=True,hwnd=0):
        try:
            self._remove_key_down_list(vk_code)
            if hwnd == 0:
                hwnd = self.hwnd
            if is_activeate:
                self.activate(hwnd)
            if isinstance(vk_code, str):
                vk_code = VK_CODE[vk_code.lower()]
            scan_code = ctypes.windll.user32.MapVirtualKeyA(vk_code, 0)
            lParam = byte_list_to_int([1,0,scan_code,32])
            if self.mode == "post":
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, lParam)
            else:
                win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, lParam)

        except:
            pass
    def activate(self,hwnd=0):
        if hwnd == 0:
            hwnd = self.hwnd
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    def set_foreground_window(self,hwnd=0):

        try:
            if hwnd == 0:
                hwnd = self.hwnd
            #win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)  # 恢复窗口
            #win32gui.SetFocus(self.hwnd)
            #win32gui.SetActiveWindow(self.hwnd)
            #win32gui.PostMessage(self.hwnd, win32con.WM_SHOWWINDOW, 0, 0)
            win32gui.PostMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
            #win32gui.SetForegroundWindow(self.hwnd)
        except:
            pass
    def inactivate(self,hwnd=0):
        if hwnd == 0:
            hwnd = self.hwnd
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_INACTIVE, 0)
    def mouse_move(self, x=None, y=None,hwnd=0):
        if x is None or y is None:
            return
        x = x if isinstance(x, int) else int(x)
        y = y if isinstance(y, int) else int(y)
        lParam = win32api.MAKELONG(x, y)
        if hwnd == 0:
            hwnd = self.hwnd
        if self.mode == "post":
            win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
        else:
            win32gui.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
        self.old_x = x
        self.old_y = y
    def mouse_mover(self, px=None, py=None,hwnd=0):
        if px is None or py is None:
            return
        px = px if isinstance(px, int) else int(px)
        py = py if isinstance(py, int) else int(py)
        # 计算新的相对位置
        new_x = self.old_x + px
        new_y = self.old_y + py
        lParam = win32api.MAKELONG(new_x, new_y)
        if hwnd == 0:
            hwnd = self.hwnd
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
        self.old_x = new_x
        self.old_y = new_y
    def mover_camera(self, px=0, py=0, centre_x=640, centre_y=360,hwnd=0):
        if hwnd == 0:
            hwnd = self.hwnd
        self.activate(hwnd)
        self.set_foreground_window(hwnd)
        self.mouse_move(centre_x, centre_y,hwnd)
        px = px if isinstance(px, int) else int(px)
        py = py if isinstance(py, int) else int(py)
        # 计算新的相对位置
        new_x = self.old_x + px
        new_y = self.old_y + py
        self.mouse_move(px,py,hwnd)
        self.old_x = new_x
        self.old_y = new_y
    def key_press(self, vk_code=0, sleep=0.04,is_activeate=True,hwnd=0):
        self.key_down(vk_code,is_activeate=True,hwnd=hwnd)
        time.sleep(sleep)
        self.key_up(vk_code,is_activeate=True,hwnd=hwnd)
    def mouse_left_click(self,x=None,y=None ,sleep=0.08,hwnd=0):
        self.mouse_left_down(x,y,hwnd=hwnd)
        time.sleep(sleep)
        self.mouse_left_up(x,y,hwnd=hwnd)
    def mouse_right_click(self, x=None,y=None,sleep=0.08,hwnd=0):
        self.mouse_right_down(x,y,hwnd=hwnd)
        time.sleep(sleep)
        self.mouse_right_up(x,y,hwnd=hwnd)
    def mouse_middle_click(self, x=None,y=None,sleep=0.08,hwnd=0):
        self.mouse_middle_down(x,y,hwnd=hwnd)
        time.sleep(sleep)
        self.mouse_middle_up(x,y,hwnd=hwnd)
# 前台键鼠实现
class MoNiForeground(MoNiInterface):
    def __init__(self, hwnd=0,mode="windows"):
        super().__init__(hwnd)
        self.hwnd = hwnd
        self.p_left = 0
        self.p_top = 0
        self.mode=mode
        self.window_width = 0
        self.window_height = 0
        self.window_border_width =0 # 左边框宽度
        self.window_title_bar_height = 0  # 标题栏高度
        self.window_bottom_border = 0  # 下边框高度
        self.bind(self.hwnd)
        # 获取当前屏幕宽度和高度
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.send = ctypes.windll.user32.SendInput
    def bind(self, hwnd):
        self.hwnd = hwnd
        if self.hwnd != 0:
            # 获取窗口的屏幕坐标（包含边框和标题栏）
            rect = win32gui.GetWindowRect(hwnd)

            # 获取客户区尺寸（这里的left/top始终为0，right/bottom是客户区宽高）
            client_rect = win32gui.GetClientRect(hwnd)

            # 将客户区左上角坐标转换为屏幕坐标
            pt_origin = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))

            # 将客户区右下角坐标转换为屏幕坐标
            pt_end = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))

            # 计算实际物理尺寸
            self.window_width = pt_end[0] - pt_origin[0]
            self.window_height = pt_end[1] - pt_origin[1]

            # 直接使用转换后的客户区坐标
            self.p_left = pt_origin[0]
            self.p_top = pt_origin[1]

            # 以下参数按需保留（如需获取边框尺寸）
            self.window_border_width = rect[0] - pt_origin[0]  # 左边框宽度
            self.window_title_bar_height = rect[1] - pt_origin[1]  # 标题栏高度
            self.window_bottom_border = rect[3] - pt_end[1]  # 下边框高度

        else:
            self.window_width = 0
            self.window_height = 0
            self.window_border_width = 0  # 左边框宽度
            self.window_title_bar_height = 0  # 标题栏高度
            self.window_bottom_border = 0  # 下边框高度
            self.p_left = 0
            self.p_top = 0
    def reset(self):
        self.bind(self.hwnd)
    def mouse_move(self, x=0, y=0):
        x = x + self.p_left
        y = y + self.p_top
        if self.mode == "dx":
            self.mouse_move3(x, y)
        elif self.mode == "windows2":
            self.mouse_move3(x, y)
        else:

            # 计算目标位置的绝对坐标值
            absolute_x = int(x / self.screen_width * 65535)
            absolute_y = int(y / self.screen_height * 65535)
            # 构造输入事件列表
            inputs = [INPUT(type=0, input=INPUT._INPUT(
                mi=MOUSEINPUT(dx=absolute_x, dy=absolute_y, mouseData=0,
                              dwFlags=win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
                              time=0, dwExtraInfo=None)))]
            # 发送输入事件
            self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_move3(self, x=0, y=0):
        pydirectinput.moveTo(x, y,_pause=False)
    def mouse_mover(self, dx=0, dy=0):

        if self.mode == "dx":
            self.mouse_mover3(dx, dy)
        elif self.mode == "windows2":
            self.mouse_mover3(dx, dy)
        else:
            # 构造输入事件列表
            inputs = [INPUT(type=0, input=INPUT._INPUT(
                mi=MOUSEINPUT(dx=dx, dy=dy, mouseData=0, dwFlags=win32con.MOUSEEVENTF_MOVE, time=0, dwExtraInfo=None)))]
            # 发送输入事件
            self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_mover3(self, dx=0, dy=0):
        pydirectinput.moveRel(dx, dy,relative=True,_pause=False)
    def mouse_wheel(self, count=120,x=None,y=None,*args):
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0 , mouseData=count, dwFlags=win32con.MOUSEEVENTF_WHEEL, time=0, dwExtraInfo=None)
        ))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_middle_down(self,x=None,y=None,*args):
        self._add_mouse_down_list("middle")
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_MIDDLEDOWN, time=0, dwExtraInfo=None)
        ))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_middle_up(self,x=None,y=None,*args):
        self._remove_mouse_down_list("middle")
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_MIDDLEUP, time=0, dwExtraInfo=None)
        ))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_left_down(self,x=None,y=None,*args):
        self._add_mouse_down_list("left")
        if x is not None and y is not None:
           self.mouse_move(x,y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_LEFTDOWN, time=0, dwExtraInfo=None)
        ))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_left_up(self,x=None,y=None,*args):
        self._remove_mouse_down_list("left")
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_LEFTUP, time=0, dwExtraInfo=None)))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_right_down(self,x=None,y=None,*args):
        self._add_mouse_down_list("right")
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_RIGHTDOWN, time=0, dwExtraInfo=None)
        ))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_right_up(self,x=None,y=None,*args):
        self._remove_mouse_down_list("right")
        if x is not None and y is not None:
            self.mouse_move(x, y)

        inputs = [INPUT(type=0, input=INPUT._INPUT(
            mi=MOUSEINPUT(dx=0, dy=0, mouseData=0, dwFlags=win32con.MOUSEEVENTF_RIGHTUP, time=0, dwExtraInfo=None)))]
        # 发送输入事件
        self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def mouse_left_click(self,x=None,y=None, sleep=0.08):
        self.mouse_left_down(x,y)
        time.sleep(sleep)
        self.mouse_left_up(x,y)
    def mouse_right_click(self,x=None,y=None, sleep=0.08):
        self.mouse_right_down(x,y)
        time.sleep(sleep)
        self.mouse_right_up(x,y)
    def mouse_middle_click(self,x=None,y=None, sleep=0.08):
        self.mouse_middle_down(x,y)
        time.sleep(sleep)
        self.mouse_middle_up(x,y)
    def key_down(self, vk_code=0):
        self._add_key_down_list(vk_code)
        if self.mode=="dx":
            self.key_down3(vk_code=vk_code)
        elif self.mode == "windows2":
            self.key_down2(vk_code=vk_code)
        else:
            if type(vk_code) == str:
                vk_code = VK_CODE[vk_code.lower()]
            inputs = [INPUT(type=1, input=INPUT._INPUT(
                ki=KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=0, time=0, dwExtraInfo=None)))]
            # 发送输入事件
            self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    def key_up(self, vk_code=0):
        self._remove_key_down_list(vk_code)
        if self.mode == "dx":
            self.key_up3(vk_code=vk_code)
        elif self.mode == "windows2":
            self.key_up2(vk_code=vk_code)
        else:
            if type(vk_code) == str:
                vk_code=VK_CODE[vk_code.lower()]
            inputs = [INPUT(type=1, input=INPUT._INPUT(
                ki=KEYBDINPUT(wVk=vk_code, wScan=0, dwFlags=win32con.KEYEVENTF_KEYUP, time=0, dwExtraInfo=None)))]
            # 发送输入事件
            self.send(len(inputs), ctypes.byref(inputs[0]), ctypes.sizeof(INPUT))
    @staticmethod
    def key_down2(vk_code=0):
        if type(vk_code) == str:
            vk_code=VK_CODE[vk_code.lower()]
        win32api.keybd_event(vk_code, 0, 0, 0)
    @staticmethod
    def key_up2(vk_code=0):
        if type(vk_code) == str:
            vk_code=VK_CODE[vk_code.lower()]
        win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    @staticmethod
    def key_down3(vk_code=0):
        pydirectinput.keyDown(vk_code,_pause=False)
    @staticmethod
    def key_up3(vk_code=0):
        pydirectinput.keyUp(vk_code,_pause=False)
    def key_press(self, vk_code=0, sleep=0.04):
        if self.mode == "dx":
            self.key_press3(vk_code=vk_code,sleep=sleep)
        elif self.mode == "windows2":
            self.key_press2(vk_code=vk_code,sleep=sleep)
        else:
            self.key_down(vk_code)
            time.sleep(sleep)
            self.key_up(vk_code)
    def key_press2(self, vk_code=0, sleep=0.04):
        self.key_down2(vk_code)
        time.sleep(sleep)
        self.key_up2(vk_code)
    def key_press3(self, vk_code=0, sleep=0.04):
        '''
        模拟按键按下和释放 directinput 的方式
        :param vk_code:
        :param sleep:
        :return:
        '''
        self.key_down3(vk_code)
        time.sleep(sleep)
        self.key_up3(vk_code)
#这里可以继续写更多键鼠的实现类-----
#-------------

# 模拟键鼠工厂
class MoNi():

    def create(self, hwnd: int, mode: int = 0):
        '''

        :param hwnd:
        :param mode: 1 前台模式 2. 前台模式二  3. dx前台模式 4.后台消息模式  1 2 3都是前台模式 如果遇到无法控制的可以挨个尝试
        :return:
        '''
        if mode == 0:
            return MoNiForeground(hwnd,mode="windows")
        if mode == 1:
            return MoNiForeground(hwnd,mode="windows2")
        if mode == 2:
            return MoNiForeground(hwnd,mode="dx")
        if mode == 3:
            return MoNiBackstage(hwnd,mode="post")
        if mode == 4:
            return MoNiBackstage(hwnd,mode="send")
        else:
            raise Exception("mode error")