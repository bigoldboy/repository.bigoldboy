#0702 Youtube video (needs exteral player YOUTUBE)
#0703 Youtube playlist (needs exteral player YOUTUBE)
#0704 Youtube channel (needs exteral player YOUTUBE)
#0900 VaderStreams
#0991 Vader Catchup
#0902 USAIPTV
#0997 SportsAccess
#0999 SmoothStreams
#1000 Direct URL

import urllib, urllib2, re, os, json, xbmc, xbmcgui, xbmcaddon, xbmcplugin, time, sys, liveresolver, xbmcvfs, BeautifulSoup
from os.path import isfile, join
from StringIO import StringIO ; from datetime import timedelta ; from bigoldboy import *   # biggy's functions
from resources.lib import createurl ; from resources.lib import livestream

showdebug=True  # Extra debug points written to ron.log

selfAddon = xbmcaddon.Addon(id='plugin.video.bobtv') # points to our addon
USER_AGENT    = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
stdHeaders = {'User-Agent':USER_AGENT, 'Accept':"*/*", 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8'}
pDialog = xbmcgui.DialogProgress()
addon = xbmcaddon.Addon()
addon_url = sys.argv[0]                   # Get the plugin url (plugin://plugin.video.bobcollection/)
addon_handle = int(sys.argv[1])           # Get the plugin handle as an integer number. (interger)
addon_name = addon.getAddonInfo('name')   # Get the addon name (bobcollection)
addon_id = addon.getAddonInfo('id')       # Get the addon id (plugin.video.bobcollection)
addon_path = addon.getAddonInfo('path')   # C:\Users\rondyer\Dropbox\Kodibox\portable_data\addons\plugin.video.bobcollection
addon_handle=int(sys.argv[1]) # Create Directory
path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.bobtv/'))

title="Launching bob.tv"
progress_create("bobtv",str.center(title,119-len(title),' '))          
#####################################################################################
#                   Define COMMON Subroutines Used By All Services                  #
#####################################################################################
def get_params(): # What parameters have been passed? 
    
    param = [] ; paramstring = sys.argv[2]
    if len(paramstring) >= 2:  # see if we have anything. first char is ? 
        params = sys.argv[2][1:]   # load string passed into var params
        cleanedparams = params.replace('', '')  # clean up the params 
        if (params[len(params) - 1] == '/'): params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2: param[splitparams[0]] = splitparams[1]    
    return param

def get_iconimage():    
    
    if len(extra)>0 and "radiostation" in name : return extra  #if supplied (usually radio) 
    iname=name.strip() 
    if "Channel #" in iname: iname="Sports Channel #"
    if iname[:12] == "Vader Sports":iname="Match Centre Event"     
    if " HD" in iname.upper(): iname = iname.replace(" HD","")         
    LogosFolderPath = selfAddon.getSetting('LogosFolderPath'); fileiconlist=LogosFolderPath+"iconlist.txt"
    if xbmcvfs.exists(fileiconlist): 
        f = xbmcvfs.File(fileiconlist) 
        contents = f.read() 
        f.close()        
        contents=re.compile('<name>(.+?)</name>.+?icon>(.+?)</icon>').findall(contents)            
        for longname,iconname in contents: 
            if iname.upper() == longname.upper():
                iname=iconname
                break
    else: ts("No Icon List")
    if xbmcvfs.exists(LogosFolderPath+str(iname)+".jpg"): iconimage = LogosFolderPath+str(iname)+".jpg"
    else: 
        if xbmcvfs.exists(LogosFolderPath+str(iname)+".png"): iconimage = LogosFolderPath+str(iname)+".png"
        else: iconimage = LogosFolderPath+"missing icon.jpg"    
    return iconimage

def get_program_title():
    if "radiostation" in name: # is it a radio station?
        if len(name) == 12: return "" # don't include a name as to allow the song info to pass through
        else: return name[13:]
    servicecolor = selfAddon.getSetting('color'+str(mode)) 
    return "[COLOR"+servicecolor+"]"+progtitle+"[/COLOR] "

def get_service_name():
    osdService = selfAddon.getSetting('osdService')             #see if we are displaying SERVICE NAME on screen
    if osdService == "false":                                   #nothing to display                
        return ""
    osdColor = selfAddon.getSetting('osdColor')                 #get the color we will set the service name to
    serviceshort = selfAddon.getSetting('serviceshort'+str(mode))
    servicelong = selfAddon.getSetting('servicelong'+str(mode))
    osdServicelong = selfAddon.getSetting('osdServicelong')     #see if using long or short service name on screen
    if osdServicelong == "true": service = "["+servicelong+"]"
    else: service = serviceshort    
    return  "[COLOR "+osdColor+"] " + service + " [/COLOR]"    

def get_station_name():
    osdColor = selfAddon.getSetting('osdColor')  ; return  "[COLOR "+osdColor+"] " + name + "[/COLOR]"    

def get_mode():
    osdMode = selfAddon.getSetting('osdMode')       
    osdColor = selfAddon.getSetting('osdColor')    
    if osdMode == "false": return  ""
    return mode 

def playlink(murl, thumb): # play the channel   
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem(thumbnailImage=thumb)
    listitem.setInfo(type="Video", infoLabels={"mediatype": "episode","episode": int(get_mode()),"tvshowtitle": get_station_name()+get_service_name(), "title": get_program_title()})
    playlist.add(murl, listitem)
    out("-------------------------------------------------------------------------")
    out("PLAYING: "+murl)
    out("-------------------------------------------------------------------------")    
    xbmc.Player().play(playlist) 
    return True    

def show_connect(which): 
    if selfAddon.getSetting('connecting'+str(mode))=="true":        
        clr = str(selfAddon.getSetting('connectingColor'+str(which)))        
        if which == 1:
            title="[COLOR "+clr+"]bob.tv is contacting the service provider[/COLOR]";banner="Contacting "+str( selfAddon.getSetting('servicelong'+str(mode)))+" (Mode "+str(mode)+")"
        else:
            if "radiostation" in name: banner = "Starting Radio Station Stream"
            else: banner=stripcolor(name)+" - "+stripcolor(progtitle)
            title="[COLOR "+clr+"]bob.tv is starting the stream[/COLOR]"
        progress_create(title,str.center(banner,126-len(banner),' '))        
        
def stripcolor(namestring):  
    x=namestring.find("[") #find first color bracket
    if x==-1: #not found
        return namestring  #no color so return
    else:  #i have at least 1 color string
        y=namestring.find("]")
        namestring=namestring[:x]+namestring[y+1:]#remove the color part
        x=namestring.find("[") #find second color bracket
        if x==-1: #no second
            return namestring.replace('[/COLOR]',"")
        else: #there are two to remove
            y=namestring.find("]")
            namestring=namestring[:x]+namestring[y+1:]#remove the color part
            return namestring.replace('[/COLOR]',"")
            
#####################################################################################
#                           Start of Addon bob.tv                                   #
#####################################################################################
if showdebug: out("\n=========== Launching  bob.tv ==============")
params = get_params(); url=""; name=None; mode=0; iconimage=None;progtitle=None;extra="";progtitle="No Program Name"
try: url = urllib.unquote_plus(params["url"]) 
except: pass
url = url.replace("~","=").replace("$","&")  # if url has an equal sign in it, it was changed to'~' so change it back
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass
try: progtitle = urllib.unquote_plus(params["title"])
except: pass
try: extra = urllib.unquote_plus(params["extra"])
except: pass
if showdebug:     
    out("** url       = "+url)
    out("** name      = "+name)
    out("** mode      = "+str(mode))
    out("** icon      = "+str(iconimage))
    out("** progtitle = "+str(progtitle))
    out("** extra     = "+extra)
    out("** full raw  = "+str(sys.argv[2]))

show_connect(1)
if mode == 702: 
    if url=="test":
        url = xbmcgui.Dialog().input("Enter YouTube Video:   ")
        progtitle="Channel "+str(url) 
    show_connect(1)
    rurl="plugin://plugin.video.youtube/play/?video_id="+str(url)+"/"
    xbmc.executebuiltin('PlayMedia(%s)' % rurl)
    
elif mode == 703: 
    if url=="test":
        url = xbmcgui.Dialog().input("Enter YouTube Playlist:   ")
        progtitle="Channel "+str(url) 
    show_connect(1)
    rurl="plugin://plugin.video.youtube/playlist/"+str(url)+"/"
    xbmc.executebuiltin('ActivateWindow(10025,'+rurl+',return)')

elif mode == 704: 
    if url=="test":
        url = xbmcgui.Dialog().input("Enter YouTube Channel:  ")
        progtitle="Channel "+str(url) 
    show_connect(1)
    rurl="plugin://plugin.video.youtube/channel/"+str(url)+"/"
    xbmc.executebuiltin('ActivateWindow(10025,'+rurl+')')

elif 989 < mode < 1011: 
    
    if mode == 990: #Vaderstreams
        if progtitle == "Match Centre Event" : name="Vader Sports Channel "+url
        if url=="test":
            url = xbmcgui.Dialog().input("Enter VaderSTREAM Channel Number: (4 digits): ")
            progtitle="Channel "+str(url)        
        show_connect(1)    
        url=createurl.get_vader(url)  

    elif mode == 991:
        show_connect(1)
        xferfile= xbmc.translatePath(join('special://logpath','vaderxfer'))
        url=readfile(xferfile)

    elif mode == 992:  #USAIPTV
        if url=="test": 
            url = xbmcgui.Dialog().input("Enter USAIPTV Channel Number: (4 digits): ")
            progtitle="Channel "+str(url)        
        show_connect(1)
        url=createurl.get_usaiptv(url)
        
    elif mode == 993:  #Livestream.com    
        owner_id = str(extra)
        event_id = str(url)
        if url=="test": 
            owner_id = xbmcgui.Dialog().input("Enter OWNERID Number:  ")
            progtitle="Channel "+str(url)                
            event_id = xbmcgui.Dialog().input("Enter EVENTID Number:  ")
            progtitle="Channel "+str(url)                
        #progtitle = str(name)+ " Local News"
        url=livestream.get_livestream(owner_id,event_id,video_id = None)   

    elif mode == 997:
        if url=="test":
            url = xbmcgui.Dialog().input("Enter SportsAccess Channel Number: (2 digits): ")
            progtitle="Channel "+str(url)
        url = createurl.sa_url(url)        

    elif mode == 999:
        if url=="test":
            url = xbmcgui.Dialog().input("Enter SmoothStreams Channel Number: (2 digits): ")
            progtitle="Channel "+str(url)        
    	url = createurl.ss_url(url)        

    elif mode == 1000:
        if url.find("181.fm")>0: #181 links need to be removed from .pls file
            newurl = readfile(url);x=newurl.find("File1=");y=newurl.find(".mp3");url=newurl[x+6:y+4]                  
        if url == "test": 
            url = xbmcgui.Dialog().input("Enter or paste Direct URL: ");progtitle="Channel "+str(url)        
    show_connect(2)
    playlink(url,get_iconimage())

elif mode == None or mode == 0: xbmc.executebuiltin('Addon.OpenSettings("plugin.video.bobtv")')
else: attention("MODE="+str(mode)+" - Mode not configured yet!") #don't know this one
