# -*- coding: utf-8 -*-

import os
import settings
import time
import threading

from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetLogoDir
from Plugins.Extensions.IPTVPlayer.components.ihost import IHost, CDisplayListItem, RetHost, CUrlItem, ArticleContent, CFavItem

########################################################
def formSUBMITvalue( inputHiddenObjects, caption, input_def = '', input_text = '' ):
	retTxt = '\n<form method="GET">%s' % input_text
	for inputObj in inputHiddenObjects:
		retTxt += '<input type="hidden" name="%s" value="%s">' % (inputObj[0], inputObj[1])
	retTxt += '<input type="submit" value="%s" %s></form>\n' % (caption, input_def)
	return retTxt
########################################################
def formGET( radioList ):
	radioList = radioList.strip()
	if radioList.endswith('</br>'):
		radioList = radioList[:-5]
	elif radioList.endswith('<br>'):
		radioList = radioList[:-4]
	if radioList.startswith('ERROR:'):
		return '\n<a><font color="#FFE4C4">%s</font></a>' % (radioList[6:])
	elif radioList.count('<input type="radio"') == 1:
		return '%s' % (radioList)
	else:
		return '\n<form method="GET">\n%s\n<input type="submit" value="%s"></form>\n' % (radioList, _('Save'))
########################################################
def removeSpecialChars(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace('"', "'").replace('  ', " ").strip()
    text = text.replace('&oacute;', 'ó').replace('&Oacute;', 'Ó')
    text = text.replace('&quot;', "'").replace('&#34;', "'").replace('&nbsp;', ' ').replace('&#160;', " ").replace('[/br]', "<br>")
    return text.strip()
########################################################
def getHostLogo(hostName):
	try:
		_temp = __import__('Plugins.Extensions.IPTVPlayer.hosts.host' + hostName, globals(), locals(), ['IPTVHost'], -1)
		logo = _temp.IPTVHost().getLogoPath().value[0]
		_temp = None
		if os.path.exists(logo):
			logo = '<img border="0" alt="hostLogo" src="./icons/logos/%s" width="120" height="40">' % logo.replace(GetLogoDir(),'')
		else:
			raise Exception
	except Exception:
		if os.path.exists(GetLogoDir('%slogo.png' % hostName)):
			logo = '<img border="0" alt="hostLogo" src="./icons/logos/%slogo.png" width="120" height="40">' % hostName
		else:
			logo = ""
	return logo
########################################################
def initActiveHost( hostName ):
	settings.activeHost = {}
	settings.retObj = None
	settings.currItem = {}
	
	if hostName is None:
		pass
	else:
		
		settings.activeHost['Name'] = hostName
		_temp = __import__('Plugins.Extensions.IPTVPlayer.hosts.host' + hostName, globals(), locals(), ['IPTVHost'], -1)
		settings.activeHost['Title'] = _temp.gettytul()
		settings.activeHost['Obj'] = _temp.IPTVHost()
		settings.activeHost['PIC'] = settings.activeHost['Obj'].getLogoPath().value[0]
		settings.activeHost['SupportedTypes'] = settings.activeHost['Obj'].getSupportedFavoritesTypes().value
		settings.activeHost['PathLevel'] = 1
		settings.activeHost['Status'] =  ''
		settings.retObj = settings.activeHost['Obj'].getInitList()
		settings.activeHost['ListType'] = 'ListForItem'
	return
########################################################
def isActiveHostInitiated():
	if len(settings.activeHost.keys()) == 0:
		return False
	else:
		return True
########################################################
def isCurrentItemSelected():
	if len(settings.currItem.keys()) == 0:
		return False
	else:
		return True
########################################################
def iSactiveHostsHTMLempty():
	if len(settings.activeHostsHTML.keys()) == 0:
		return True
	else:
		return False
########################################################
def isConfigsHTMLempty():
	if len(settings.configsHTML.keys()) == 0:
		return True
	else:
		return False
########################################################
def isNewHostListShown():
	return settings.NewHostListShown

########################################################
def setNewHostListShown(status):
	settings.NewHostListShown = status
########################################################
def isThreadRunning(name):
	status = False
	for i in threading.enumerate():
		#print 'isThreadRunning>running threads:' , i.name
		if name == i.name:
			status = True
	return status
########################################################
def stopRunningThread(name):
	for myThread in threading.enumerate():
		#print 'isThreadRunning>running threads:' , i.name
		if name == myThread.name:
			if (myThread.isAlive()):
				myThread.terminate()
	time.sleep(0.2) #time for thread to close
	return isThreadRunning(name)
