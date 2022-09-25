# -*- coding: utf-8 -*-
import threading
import sys
import ntchat
import subprocess
import os
import win32api
import pyautogui
import time

TIMING = 20*60

import ctypes
import inspect
# python 2/3 switch
try:
    import thread
except ImportError:
    import _thread as thread
import threading

name = "kthread"

def _async_raise(tid, exctype):
    """Raises the exception, causing the thread to exit"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread ID")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class KThread(threading.Thread):
    """Killable thread.  See terminate() for details"""
    def _get_my_tid(self):
        """Determines the instance's thread ID"""
        if not self.is_alive():
            raise threading.ThreadError("Thread is not active")
        
        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id
        
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        
        raise AssertionError("Could not determine the thread's ID")
    
    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)
    
    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        # WARNING: using terminate(), kill(), or exit() can introduce instability in your programs
        # It is worth noting that terminate() will NOT work if the thread in question is blocked by a syscall (accept(), recv(), etc.)
        self.raise_exc(SystemExit)

    # alias functions
    def kill(self):
        self.terminate()
        
    def exit(self):
        self.terminate()

mitmproxy_path = input("MitmDump路径:")

port = 8886

if os.name != "nt":
    print("该脚本仅支持Windows，其他操作系统上无效。")
    exit(0)

while True:
    os.system("taskkill /f /im WeChat.exe") # 关闭微信
    os.system("taskkill /f /im WeChat.exe") # 关闭微信
    os.system("taskkill /f /im WeChat.exe") # 关闭微信

    wechat = ntchat.WeChat()

    # 打开pc微信, smart: 是否管理已经登录的微信
    wechat.open(smart=True)

    # 等待登录
    wechat.wait_login()

    def on_exit(sig, func=None):
        ntchat.exit_()
        sys.exit()


    # 当关闭cmd窗口时
    win32api.SetConsoleCtrlHandler(on_exit, True)

    csbs = "gh_8838a095be4a" # 穿梭巴士的wxid

    wechat.send_text(to_wxid=csbs, content="你好，小金！我想买票。") # 这是为了将公众号浮到微信联系人第一行

    print("发完了")

    time.sleep(5)

    print("移动到巴士购票公众号")
    pyautogui.moveTo(x=559, y=171)
    #pyautogui.moveTo(x=546, y=254)
    pyautogui.click()

    def x():
        try:
            print("运行代理中")
            myMITm = subprocess.run(f"\"{mitmproxy_path}\" -p {port} -s script.py", check=True)
        except Exception:
            pass
    x_1 = KThread(target=x)
    x_1.start()
    def y():
        print("设置代理")
        myBat = f"""
        reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
        reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f
        reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f
        taskkill /f /im SystemSettings.exe & start ms-settings:network-proxy
        taskkill /f /im SystemSettings.exe
        reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d 127.0.0.1:{port} /f
        taskkill /f /im iexplorer.exe && start /w /b iexplorer.exe
        taskkill /f /im iexplorer.exe
        reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
        taskkill /f /im iexplorer.exe && start /w /b iexplorer.exe
        taskkill /f /im iexplorer.exe
        """

        with open("myp.bat", "w") as bat:
            bat.write(myBat)

        try:
            def ade():
                subprocess.run("cmd /c myp.bat", check=True)
            myMitm = KThread(target=ade)
            myMitm.start()
            time.sleep(3)
            print("移动到车票购买")
            pyautogui.moveTo(x=883, y=949)
            pyautogui.click()
            print("点击穿梭巴士")
            pyautogui.moveTo(x=879,y=781)
            pyautogui.click()
        except Exception:
            pass
    y_1=KThread(target=y)
    y_1.start()
    time.sleep(TIMING+20)