from pynput import keyboard
from pynput import mouse


class HookKeyMouse:
    # 类级别的事件处理函数列表
    _key_press_handlers = []
    _key_release_handlers = []
    _mouse_click_handlers = []
    _mouse_scroll_handlers = []
    _mouse_move_handlers = []

    # 类级别的监听器实例
    _keyboard_listener = None
    _mouse_listener = None

    def __init__(self, hookMouse=False, hookKey=True):
        """
        初始化时自动注册被重写的事件处理方法。
        """
        self.hookMouse = hookMouse
        self.hookKey = hookKey

        # 注册键盘事件处理函数
        if self.hookKey:
            if self.__class__.on_press != HookKeyMouse.on_press:
                HookKeyMouse._key_press_handlers.append(self.on_press)
            if self.__class__.on_release != HookKeyMouse.on_release:
                HookKeyMouse._key_release_handlers.append(self.on_release)

        # 注册鼠标事件处理函数
        if self.hookMouse:
            if self.__class__.on_click != HookKeyMouse.on_click:
                HookKeyMouse._mouse_click_handlers.append(self.on_click)
            if self.__class__.on_scroll != HookKeyMouse.on_scroll:
                HookKeyMouse._mouse_scroll_handlers.append(self.on_scroll)
            if self.__class__.on_move != HookKeyMouse.on_move:
                HookKeyMouse._mouse_move_handlers.append(self.on_move)

    def on_press(self, key):
        pass

    def on_release(self, key):
        pass

    def on_click(self, x, y, button, pressed):
        pass

    def on_scroll(self, x, y, dx, dy):
        pass

    def on_move(self, x, y):
        pass

    # 类方法作为实际的事件回调，分发给所有处理函数
    @classmethod
    def _on_press(cls, key):
        for handler in cls._key_press_handlers:
            handler(key)

    @classmethod
    def _on_release(cls, key):
        for handler in cls._key_release_handlers:
            handler(key)

    @classmethod
    def _on_click(cls, x, y, button, pressed):
        for handler in cls._mouse_click_handlers:
            handler(x, y, button, pressed)

    @classmethod
    def _on_scroll(cls, x, y, dx, dy):
        for handler in cls._mouse_scroll_handlers:
            handler(x, y, dx, dy)

    @classmethod
    def _on_move(cls, x, y):
        for handler in cls._mouse_move_handlers:
            handler(x, y)

    @classmethod
    def start_global_hook(cls):
        """启动全局钩子（只需调用一次）"""
        # 启动键盘监听器
        if cls._keyboard_listener is None:
            cls._keyboard_listener = keyboard.Listener(
                on_press=cls._on_press,
                on_release=cls._on_release
            )
            cls._keyboard_listener.start()

        # 启动鼠标监听器
        if cls._mouse_listener is None:
            cls._mouse_listener = mouse.Listener(
                on_click=cls._on_click,
                on_scroll=cls._on_scroll,
                on_move=cls._on_move
            )
            cls._mouse_listener.start()

    @classmethod
    def stop_global_hook(cls):
        """停止全局钩子"""
        if cls._keyboard_listener is not None:
            cls._keyboard_listener.stop()
            cls._keyboard_listener = None
        if cls._mouse_listener is not None:
            cls._mouse_listener.stop()
            cls._mouse_listener = None

if __name__ == '__main__':

    #这个类的目的就是可以多次实例化重写 on hook事件 又不覆盖前面的  可以实现叠加监视 方便多个不同文件不同类调用
    # 示例用法
    class MyKeyboardHook(HookKeyMouse):
        def on_press(self, key):
            print(f"1键盘按下: {key}")

    class MyMouseHook(HookKeyMouse):
        def on_press(self, key):
            print(f"2键盘按下: {key}")
    # 创建实例并注册处理函数
    kb_hook =   MyKeyboardHook(hookKey=True, hookMouse=False)
    mouse_hook = MyMouseHook( hookKey=True,hookMouse=False)
    # 启动全局钩子
    HookKeyMouse.start_global_hook()
    # 保持主线程运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        HookKeyMouse.stop_global_hook()
