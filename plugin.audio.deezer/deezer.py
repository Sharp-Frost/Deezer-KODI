"""
XBMC Addon Developer's Guide
Example 1 - The basic plugin structure
Demonstrates creating a static list

NB This is done using functions - you could use classes
Author: Ashley Kitson
"""

# Step 1 - load in xbmc core support and setup the environment
import sys, os, shutil, re, pickle, time, tempfile, xbmcaddon, xbmcplugin, xbmcgui, xbmc
from DeezerAPI import DeezerAPI

__addon__     = xbmcaddon.Addon('plugin.audio.deezer')
__language__  = __addon__.getLocalizedString
__debugging__  = __addon__.getSetting('debug')
__cwd__       = __addon__.getAddonInfo('path')

baseDir = __cwd__
resDir = xbmc.translatePath(os.path.join(baseDir, 'resources'))
imgDir = xbmc.translatePath(os.path.join(resDir,  'img'))
deezerApi = DeezerAPI()

#Image resources
searchImg = xbmc.translatePath(os.path.join(imgDir, 'search.png'))
searchArtistImg= xbmc.translatePath(os.path.join(imgDir, 'searchArtist.png'))
searchAlbumImg= xbmc.translatePath(os.path.join(imgDir, 'searchAlbum.png'))
radioImg= xbmc.translatePath(os.path.join(imgDir, 'radio.png'))
authImg= xbmc.translatePath(os.path.join(imgDir, 'auth.png'))
myMusic= xbmc.translatePath(os.path.join(imgDir, 'myMusic.png'))
myPlaylists= xbmc.translatePath(os.path.join(imgDir, 'myPlaylists.png'))
myAlbums= xbmc.translatePath(os.path.join(imgDir, 'myAlbums.png'))

if __debugging__ == 'true':
	__debugging__ = True
else:
	__debugging__ = False


# Get entry from keyboard
def readKeyboard(queryText):
	kb = xbmc.Keyboard("", queryText, False)
	kb.doModal()
	if (kb.isConfirmed() and len(kb.getText()) > 2):
		return kb.getText()

# Read command-line parameters
def getParams():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

#Main
print("Args:"+sys.argv[2])
params=getParams()
try:
	print(str(params))
	if "mode" in params:
		mode = params["mode"]
	else:
		mode = ""
	if "idItem" in params:
		idItem = params["idItem"]
	if "link" in params:
		link=params["link"]
except:
	print('!! EXCEPTION CAUGHT !!')
	mode = 0
	

if mode=="searchArtist":
	searchWord = readKeyboard(__language__(50008))
	if searchWord!=None:
		deezerApi.searchArtist(searchWord)

elif mode == "search":
	searchWord = readKeyboard(__language__(50007))
	if searchWord!=None:
		deezerApi.search(searchWord)

elif mode=="searchAlbum":
	searchWord=readKeyboard(__language__(50009))
	if searchWord!=None:
		deezerApi.searchAlbum(searchWord)

elif mode=="radio":
	searchWord=readKeyboard(__language__(50010))
	deezerApi.searchRadio(searchWord)
	
elif mode =="resultSearchArtist":
	deezerApi.searchArtistAlbums(idItem)
	
elif mode =="resultSearchAlbum":
	deezerApi.searchAlbumSongs(idItem)
	
elif mode =="myMusic":
	u = "%s?mode=myPlaylists" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50014), iconImage=myPlaylists, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	u = "%s?mode=myAlbums" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50015), iconImage=myAlbums, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
elif mode =="myPlaylists":
	deezerApi.getMyPlaylists()
	
elif mode =="myAlbums":
	deezerApi.getMyAlbums()
	
elif mode == "playlist":
	deezerApi.getPlaylistTracks(idItem)

elif mode == "next":
	print('link:'+link)
	deezerApi.getNext(link)

#Welcome menu
else:
	u = "%s?mode=myMusic" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50013), iconImage=myMusic, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
	u = "%s?mode=search" % (sys.argv[0],) 
	liz=xbmcgui.ListItem(__language__(50000), iconImage=searchImg, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
	u = "%s?mode=searchArtist" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50001), iconImage=searchArtistImg, thumbnailImage="")  
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
	u = "%s?mode=searchAlbum" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50002), iconImage=searchAlbumImg, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
	u = "%s?mode=radio" % (sys.argv[0],)
	liz=xbmcgui.ListItem(__language__(50003), iconImage=radioImg, thumbnailImage="")
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))

