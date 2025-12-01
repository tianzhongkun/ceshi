# -*- coding: utf-8 -*-
import os
import random
import time
import traceback
import numpy as np
import win32gui
from ctypes import windll
import win32ui
import win32con
from PIL import Image

def has_title_bar(hwnd):
    # 获取窗口样式
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)

    # 判断是否有标题栏
    has_title = (style & win32con.WS_CAPTION) == win32con.WS_CAPTION

    return has_title


def screenshot(hwnd, left=0, top=0, right=0, bottom=0, filename=None,is_top=False):
    try:
        if not is_top:

            rect=win32gui.GetClientRect(hwnd)
            width=rect[2]-rect[0]
            height=rect[3]-rect[1]
            #old_time=time.time()

            # 判断窗口是否可见
            if not win32gui.IsWindowVisible(hwnd):
                return None
            # 创建设备描述表
            hwnd_dc = win32gui.GetDC(hwnd)   #GetWindowDC
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()

            # 创建位图对象
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)

            # 将位图对象绑定到设备描述表
            save_dc.SelectObject(save_bitmap)
            result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(),3)   #0  1 或者3  3没有透明通道信息
            if result == 0:
               return None
            # 将截图保存到位图对象中
            #save_dc.BitBlt((0, 0), (width, height), mfc_dc, (left, top), win32con.SRCCOPY)#win32con.CAPTUREBLT  win32con.SRCCOPY
            # 将位图对象转换为OpenCV图像
            bmp_info = save_bitmap.GetInfo()
            bmp_str = save_bitmap.GetBitmapBits(True)
            img = np.frombuffer(bmp_str, dtype='uint8').reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))
            img=img[top:bottom, left:right]
            if filename is not None:
                # 提取文件夹路径
                folder_path = os.path.dirname(filename)
                # 检查文件夹是否存在，如果不存在则创建
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                # 保存位图对象到文件
                img_pil = Image.fromarray(img[..., [2, 1, 0]])
                img_pil.save(filename, format='JPEG', quality=90)


            # 删除对象，释放资源
            save_dc.DeleteDC()

            win32gui.ReleaseDC(hwnd, hwnd_dc)
            win32gui.DeleteObject(save_bitmap.GetHandle())
            #print(time.time()-old_time)
            return img
        else:
            #old_time = time.time()
            if has_title_bar(hwnd):
                window_rect = win32gui.GetWindowRect(hwnd)
                client_rect = win32gui.GetClientRect(hwnd)

                # 计算非客户区域的尺寸
                title_bar_width = (window_rect[2] - window_rect[0]) - (client_rect[2] - client_rect[0])
                title_bar_height = (window_rect[3] - window_rect[1]) - (client_rect[3] - client_rect[1])


                width = (right - left)
                height = (bottom - top)
                left=left+window_rect[0]+title_bar_width-8
                top=top+window_rect[1]+title_bar_height-8
            else:
                rect = win32gui.GetWindowRect(hwnd)
                width = (right - left)
                height = (bottom - top)
                left = left + rect[0]
                top = top + rect[1]


            # 获取桌面窗口的句柄
            hdesktop = win32gui.GetDesktopWindow()

            # 获取设备上下文
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)

            # 创建一个兼容DC
            mem_dc = img_dc.CreateCompatibleDC()

            # 创建一个位图对象
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)

            # 将位图选入内存DC
            mem_dc.SelectObject(screenshot)

            # 使用BitBlt函数从屏幕复制到内存DC
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

            # 将位图保存为文件


            # 将位图对象转换为OpenCV图像
            bmp_info = screenshot.GetInfo()
            bmp_str = screenshot.GetBitmapBits(True)
            img = np.frombuffer(bmp_str, dtype='uint8').reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))

            if filename is not None:
                # 保存位图对象到文件
                img_pil = Image.fromarray(img[..., [2, 1, 0]])
                img_pil.save(filename, format='JPEG', quality=90)

            # 释放对象
            mem_dc.DeleteDC()
            win32gui.DeleteObject(screenshot.GetHandle())
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            #print(time.time()-old_time,img.shape)
            return img



    except :
        #print(traceback.format_exc())
        return None
















