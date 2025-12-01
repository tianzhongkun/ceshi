import ctypes
import sys
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication
import setting
from page.page_update import FormUpdate
from tools.check_update import CheckUpdate
from tools.utils import is_compiled

def load_qss(file_path):
    file = QFile(file_path)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print("无法打开文件")
        return ""
    stylesheet = file.readAll().data().decode()
    return stylesheet
if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = QApplication(sys.argv)  # 初始化Qt应用
        # 加载皮肤
        qss = load_qss('datas/app.qss')
        app.setStyleSheet(qss)
        if is_compiled():
            jcu = CheckUpdate("https://note.youdao.com/ynoteshare/index.html?id=9de0d86b9d10064ffcc95e88db6da1ac",
                              "https://note.youdao.com/ynoteshare/index.html?id=d5fabd95a17a30069c33bb1f46d6dcbb")
            vardata = jcu.get_var_data()
            if vardata:
                updatetxt = jcu.get_updatetxt()
                if float(vardata[1]) > float(setting.ver):
                    window_update = FormUpdate()
                    if setting.mode_mn == 5:
                        window_update.set_update(updatetxt,
                                                 f"当前版本:{setting.ver}  发现新版本 V{vardata[1]} 是否需要更新?",
                                                 vardata[0], vardata[4], vardata[3])
                    else:
                        window_update.set_update(updatetxt,
                                                 f"当前版本:{setting.ver}  发现新版本 V{vardata[1]} 是否需要更新?",
                                                 vardata[0], vardata[2], vardata[3])
                    window_update.exec_()
                    is_exit = window_update.is_exit
                    if is_exit:
                        sys.exit()
        else:
            print("源码运行")

        from page.page_main import main
        #主窗口
        window_main = main()
        window_main.show()
        window_main.update_ui(setting.p_left, setting.p_top)

        if window_main.auto_tft.moni.hwnd==0:
            window_main.update_ui()

        sys.exit(app.exec_())#监听消息不关闭
    else:
        # 如果不是管理员，则请求以管理员权限重新运行程序
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
