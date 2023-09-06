import xbmc
from .addon import ADDON_NAME


def log(msg):
	xbmc.log(f"[{ADDON_NAME}] {msg}", level=xbmc.LOGDEBUG)

class busyDiag():
	def create():
		xbmc.executebuiltin('ActivateWindow(BusyDialogNoCancel)')
	
	def close():
		xbmc.executebuiltin('Dialog.Close(BusyDialogNoCancel)')
#