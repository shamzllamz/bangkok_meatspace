#!/usr/bin/env python
import sys

if sys.platform.startswith('win'):
	import win32gui, win32con
	from os import getpid, system
	from threading import Timer
elif sys.platform.startswith('darwin'):
	import subprocess

def turnOffScreen():
	if sys.platform.startswith('linux'):
		os.system("xset dpms force off")
	elif sys.platform.startswith('win'):
		def force_exit():
			pid = getpid()

		t = Timer(1, force_exit)
		t.start()
		SC_MONITORPOWER = 0xF170
		win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)
		t.cancel()
	elif sys.platform.startswith('darwin'):
		subprocess.call('echo \'tell application "Finder" to sleep\' | osascript', shell=True)

if __name__ == "__main__":
	turnOffScreen()