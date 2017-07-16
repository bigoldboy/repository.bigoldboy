import re, xbmc, urllib2,  xbmcgui, xbmcplugin

#base_url = 'http://cdn.jerryseinfeld.com/assets'
def daily_seinfeld(addon_handle):  # gives us daily seinfeld
    html = urllib2.urlopen('http://www.jerryseinfeld.com/').read()    
    for v in re.finditer('"title":"(.+?)","filename":"(.+?)"' + ',"appearance":"(.+?)","venue":"(.+?)"', html):
        title, filename, year, venue = v.groups()
        li = xbmcgui.ListItem('[COLOR white]('+year+') [COLOR yellow]'+title+"[/COLOR]"  , iconImage='http://static.tumblr.com/oog0lak/icgl5id5u/fbdf.png',thumbnailImage="http://static.tumblr.com/oog0lak/icgl5id5u/fbdf.png")
        li.setInfo(type="Video", infoLabels={"mediatype": "movie","Title":'[COLOR white]'+title+'[/COLOR]', "studio": '[COLOR yellow]'+str(year)+' - '+venue+'[/COLOR]' })
        li.setProperty("Fanart_Image",'http://matemedia.com/wp-content/uploads/2015/04/JerrySeinfeld-trans-300x229.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle,url='http://cdn.jerryseinfeld.com/assets'+"/"+str(filename)+".mp4",listitem=li)
    
    