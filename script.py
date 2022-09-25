import os
import signal
import ctypes
import time
import inspect
# python 2/3 switch
try:
    import thread
except ImportError:
    import _thread as thread
import threading

name = "kthread"
#p=0
TIMING=20*60
p=0

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
import subprocess
from urllib import parse
def request(flow):
    print("Path:",flow.request.path)
    if flow.request.path.startswith("/connect/oauth2/authorize?appid="):
        print("我找到oauth了")
        myd = parse.parse_qs(flow.request.path.split("?")[1])
        print(myd)
        def z():
            myBat = f"""reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
            reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f
            reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f
            taskkill /f /im SystemSettings.exe & start ms-settings:network-proxy
            taskkill /f /im SystemSettings.exe"""

            with open("myp.bat", "w") as bat:
                bat.write(myBat)

            subprocess.run("cmd /c myp.bat", shell=True, check=True)
        z_1=KThread(target=z)
        z_1.start()
        def z2():
            global p
            print("运行 jiehe py中")
            p = subprocess.Popen("python jiehetebieban.py " + myd["uin"][0] + " " + myd["key"][0] + " " + myd["pass_ticket"][0])
            #stdout_data = p.communicate(input=myd["uin"][0].encode("UTF-8"))[0]
            #stdout_data = p.communicate(input=myd["key"][0].encode("UTF-8"))[0]
            #stdout_data = p.communicate(input=myd["pass_ticket"][0].encode("UTF-8"))[0]
        z_2=KThread(target=z2)
        z_2.start()
        time.sleep(1)
        try:
            z_1.terminate()
        except Exception:
            pass
        time.sleep(TIMING+5)
        try:
            z_2.terminate()
        except Exception:
            pass
        print("我要结束进程了")
        print("P(这应该是PID或者是某种其他东西): ", p)
        try:
            p.kill()
        except Exception:
            print("p不是popen所以无法结束他")
        os.system("taskkill /f /im mitmdump.exe")