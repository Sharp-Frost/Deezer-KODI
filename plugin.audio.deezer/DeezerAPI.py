'''
Created on 19 juin 2012

@author: TDNQ1352
'''
from DeezerDomain import Track, Album, Artist, Playlist
from Json2Python import Json2Python
from types import InstanceType
import urllib,os,sys,xbmcaddon, xbmcplugin, xbmcgui, xbmc

__addon__     = xbmcaddon.Addon('plugin.audio.deezer')
__language__  = __addon__.getLocalizedString
__cwd__       = __addon__.getAddonInfo('path')

jsonDeserializer = Json2Python()
base_url = 'http://api.deezer.com/2.0/'
baseDir = __cwd__
access_token=None

#Images Resources:
resDir = xbmc.translatePath(os.path.join(baseDir, 'resources'))
imgDir = xbmc.translatePath(os.path.join(resDir,  'img'))
nextImg = xbmc.translatePath(os.path.join(imgDir, 'next.png'))



class DeezerAPI():
    
    def __init__(self):
        pass
    
    def getRemoteData(self,url):
        if access_token==None:
            f = urllib.urlopen(url+'&output=json')
        else:
            f = urllib.urlopen(url+'&access_token='+access_token+'&output=json')
        jsonResult=f.read()
        f.close()
        listResult =jsonDeserializer.decode(jsonResult)
        return listResult
    
    #NEXT RESULTS:
    def getNext(self,url):        
        listResult =self.getRemoteData(url)
        nbItems=0
        if 'total' in listResult:
            nbItems = listResult['total']
        if 'data' in listResult:
            i=0
            for value in listResult['data']:
                if isinstance(value,Track):
                    i=i+1
                    u =value.preview
                    liz=xbmcgui.ListItem(value.title, iconImage=value.album['cover'], thumbnailImage="") 
                    liz.setInfo( type="Music", infoLabels={ "title":value.title, "artist": value.artist['name'], "album":value.album['title'], "duration":value.duration, "tracknumber":i } )
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=nbItems)
                if isinstance(value,Playlist):
                    u = "%s?mode=playlist&idItem=%s" % (sys.argv[0],value.id)
                    liz=xbmcgui.ListItem(value.title, iconImage=value.picture, thumbnailImage="")
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        if 'next' in listResult:
            u = "%s?mode=next&link=%s" % (sys.argv[0],listResult['next'])
            liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        
    
    #PLAYLIST_TRACKS
    def getPlaylistTracks(self,idItem):
        print('DeezerAPI.getPlaylistTracks:'+str(idItem))
        listResult =self.getRemoteData(base_url+'playlist/'+idItem+'/tracks')
        nbItems=0
        if 'total' in listResult:
            nbItems = listResult['total']
        if 'data' in listResult:
            i=0
            for value in listResult['data']:
                if isinstance(value,Track):
                    i=i+1
                    u =value.preview
                    liz=xbmcgui.ListItem(value.title, iconImage=value.album['cover'], thumbnailImage="") 
                    liz.setInfo( type="Music", infoLabels={ "title":value.title, "artist": value.artist['name'], "album":value.album['title'], "duration":value.duration, "tracknumber":i } )
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=nbItems)
        if 'next' in listResult:
            u = "%s?mode=next&link=%s" % (sys.argv[0],listResult['next'])
            liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        
    #MY PLAYLISTS
    def getMyPlaylists(self):
        print('DeezerAPI.getMyPlaylists')
        listResult =self.getRemoteData(base_url+'user/me/playlists')
        nbItems=0
        if 'total' in listResult:
            nbItems = listResult['total']
        if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Playlist):
                        u = "%s?mode=playlist&idItem=%s" % (sys.argv[0],value.id)
                        liz=xbmcgui.ListItem(value.title, iconImage=value.picture, thumbnailImage="")
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        if 'next' in listResult:
            u = "%s?mode=next&link=%s" % (sys.argv[0],listResult['next'])
            liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        
    
    #MY ALBUMS
    def getMyAlbums(self):
        print('DeezerAPI.getMyAlbums')
        listResult =self.getRemoteData(base_url+'user/me/albums')
        nbItems=0
        if 'total' in listResult:
            nbItems = listResult['total']
        if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Album):
                        u = "%s?mode=resultSearchAlbum&idItem=%s" % (sys.argv[0],value.id)
                        liz=xbmcgui.ListItem(value.title, iconImage=value.cover, thumbnailImage="")
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)
        if 'next' in listResult:
            u = "%s?mode=next&link=%s" % (sys.argv[0],listResult['next'])
            liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True, totalItems=nbItems)

  
    
    #SEARCH ALBUM
    def searchAlbum(self,albumTitle):
        print('DeezerAPI.searchAlbum:'+albumTitle)
        if albumTitle!=None:
            listResult = self.getRemoteData(base_url+'search/album?q='+albumTitle)
            nbItems=0
            if 'total' in listResult:
                nbItems = listResult['total']
            if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Album):
                        u = "%s?mode=resultSearchAlbum&idItem=%s" % (sys.argv[0],value.id)
                        liz=xbmcgui.ListItem(value.title, iconImage=value.cover, thumbnailImage="")
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=nbItems)
            if 'next' in listResult:
                u = "%s?mode=resultSearchAlbum" % (sys.argv[0])
                liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=nbItems)
           
                
               
               
    
    #SEARCH ARTIST
    def searchArtist(self,artistName):
        print('DeezerAPI.searchArtist:'+artistName)
        if artistName!=None:
            listResult = self.getRemoteData(base_url+'search/artist?q='+artistName+'&output=json')
            nbItems=0
            if 'total' in listResult:
                nbItems = listResult['total']
            if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Artist):
                        u = "%s?mode=resultSearchArtist&idItem=%s" % (sys.argv[0],value.id)
                        liz=xbmcgui.ListItem(value.name, iconImage=value.picture, thumbnailImage="")
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=nbItems)
            if 'next' in listResult:
                u = "%s?mode=resultSearchArtist" % (sys.argv[0])
                liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    #Search albums linked to an artist
    def searchArtistAlbums(self,idArtist):
        print('DeezerAPI.searchArtistAlbums:'+idArtist)
        if idArtist!=None:
            listResult = self.getRemoteData(base_url+'artist/'+idArtist+'/albums&output=json')
            nbItems=0
            if 'total' in listResult:
                nbItems = listResult['total']
            if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Album):
                        u = "%s?mode=resultSearchAlbum&idItem=%s" % (sys.argv[0],value.id)
                        liz=xbmcgui.ListItem(value.title, iconImage=value.cover, thumbnailImage="")
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=nbItems)
            if 'next' in listResult:
                u = "%s?mode=resultSearchAlbum" % (sys.argv[0])
                liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
                

    # Search tracks of an album
    def searchAlbumSongs(self,idAlbum):
        print('DeezerAPI.searchAlbumSongs:'+idAlbum)
        if idAlbum!=None:
            album=self.getAlbum(idAlbum)
            listResult = self.getRemoteData(base_url+'album/'+idAlbum+'/tracks&output=json')
            nbItems=0
            if 'total' in listResult:
                nbItems = listResult['total']
            if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Track):
                        track=self.getTrack(value.id);
                        release_year=self.getReleaseYear(album.release_date)
                        u =value.preview
                        liz=xbmcgui.ListItem(value.title, iconImage=album.cover, thumbnailImage="") 
                        liz.setInfo( type="Music", infoLabels={ "title":value.title, "artist": value.artist['name'], "album":album.title, "duration":value.duration, "tracknumber":int(track.track_position), "year":release_year   } )
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=nbItems)
    
    
    #GLOBAL SEARCH
    def search(self,searchWord):
        print('DeezerAPI.search:'+searchWord)
        if searchWord!=None:
            listResult = self.getRemoteData(base_url+'search?q='+searchWord+'&output=json')
            nbItems=0
            if 'total' in listResult:
                nbItems = listResult['total']
            if 'data' in listResult:
                for value in listResult['data']:
                    if isinstance(value,Track):
                        u =value.preview
                        liz=xbmcgui.ListItem(value.title, iconImage=value.album['cover'], thumbnailImage="")
                        liz.setInfo( type="Music", infoLabels={ "artist": value.artist['name'], "album":value.album['title'], "duration":value.duration } )
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=nbItems)
            if 'next' in listResult:
                u = "%s?mode=next&link=%s" % (sys.argv[0],listResult['next'])
                liz=xbmcgui.ListItem(__language__(50011), iconImage=nextImg, thumbnailImage="")
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
                
    
    def searchRadio(self,searchWord):
        print('SearchRadio not yet implemented')
        
    #GET ALBUM
    def getAlbum(self,idAlbum):
        album = self.getRemoteData(base_url+'album/'+str(idAlbum))
        return album 
    
    #GET TRACK
    def getTrack(self,idTrack):
        track = self.getRemoteData(base_url+'track/'+str(idTrack))
        return track 
    
    # Extract Release year from a date yyyy-mm-dd
    def getReleaseYear(self,date):
        if date!=None:
            splitedDate = str(date).split('-')
            return int(splitedDate[0])
        else:
            return 1900
    
