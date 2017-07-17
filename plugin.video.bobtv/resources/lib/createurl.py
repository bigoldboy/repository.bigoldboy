import xbmcaddon
import urllib, urllib2, re, os, json, xbmc, xbmcgui, xbmcaddon, xbmcplugin, time, sys 
from StringIO import StringIO
from datetime import timedelta
from bigoldboy import *   # biggy's functions

selfAddon = xbmcaddon.Addon(id='plugin.video.bobtv') # points to our addon
##########################################################################
#          Routines used only by Mode 999 (SmoothStreams)                #
##########################################################################
def ss_url(url):
    user_agent = "Smoothstreams.tv_0.8.0%20%28Kodi%2016.1%20Git%3A20160424-c327c53%3B%20Windows%20AMD64%29%20Windows"
    channel = url # determined earlier
    SmoothStreamPassword    = selfAddon.getSetting('SmoothStreamPassword')
    SmoothStreamUserName    = selfAddon.getSetting('SmoothStreamUserName')
    SmoothStreamPortRTMP    = selfAddon.getSetting('SmoothStreamPortRTMP')
    SmoothStreamPortHLS     = selfAddon.getSetting('SmoothStreamPortHLS')
    SmoothStreamSite        = selfAddon.getSetting('SmoothStreamSite')
    SmoothStreamServer      = selfAddon.getSetting('SmoothStreamServer')
    SmoothStreamHLS         = selfAddon.getSetting('SmoothStreamHLS')
    
    if SmoothStreamServer == "0":       SmoothStreamServer = "dEU.SmoothStreams.tv" # EU Random 12.70
    elif SmoothStreamServer == "1":     SmoothStreamServer = "dEU.NL1.SmoothStreams.tv"  # EU (NL-i3d) 5.33,11.44,4.50
    elif SmoothStreamServer == "2":     SmoothStreamServer = "dEU.UK.SmoothStreams.tv"   # EU (UK-London) 12.82
    elif SmoothStreamServer == "3":     SmoothStreamServer = "dNAe.SmoothStreams.tv"     # US East 3.21, 2.78, 3.81
    elif SmoothStreamServer == "4":     SmoothStreamServer = "dNAw.SmoothStreams.tv"     # US West 4.45
    elif SmoothStreamServer == "5":     SmoothStreamServer = "dNA.SmoothStreams.tv"      # US Random All 4.26
    elif SmoothStreamServer == "6":     SmoothStreamServer = "dSG.SmoothStreams.tv"      # Asia didn't work
    elif SmoothStreamServer == "7":     SmoothStreamServer = "dEU.NL2.SmoothStreams.tv"  # EU (NL-Evo) didn't work
    elif SmoothStreamServer == "8":     SmoothStreamServer = "dNAE1.SmoothStreams.tv"    # US East-NJ 11.61
    elif SmoothStreamServer == "9":     SmoothStreamServer = "dNAE2.SmoothStreams.tv"    # US East-VA 4.35
    elif SmoothStreamServer == "10":    SmoothStreamServer = "dNAE3.SmoothStreams.tv"    # US East-CAN 3.88, 2.93, 3.55
    elif SmoothStreamServer == "11":    SmoothStreamServer = "dNAE4.SmoothStreams.tv"    # US East-CAN2 4.86
    elif SmoothStreamServer == "12":    SmoothStreamServer = "dEU.DE1.SmoothStreams.tv"  # EU DE Frankfurt 5.73
    elif SmoothStreamServer == "13":    SmoothStreamServer = "dNAw1.SmoothStreams.tv"  # EU DE Frankfurt 5.73
    else: attention("ERROR Undefined Server - "+ SmoothStreamServer)
    shash = readurl("http://smoothstreams.tv/schedule/admin/dash_new/hash_api.php?site=" +str(SmoothStreamSite)+"&username="+SmoothStreamUserName+"&password="+SmoothStreamPassword)
    shash = shash[9:len(shash)-25]
    if SmoothStreamHLS == "true": return 'http://'+ str(SmoothStreamServer) + ':' + str(SmoothStreamPortHLS) + "/" + str(SmoothStreamSite) + "/ch" + str(channel) + "q1.stream/playlist.m3u8?wmsAuthSign=" + str(shash) +"|User-Agent=Smoothstreams.tv/0.8.1%20%28Kodi%2016.1%20Git%3A20160424-c327c53%3B%20Windows%20AMD64%29%20Windows"
    else: return 'rtmp://'+ str(SmoothStreamServer) + ':' + str(SmoothStreamPortRTMP) + "/" + str(SmoothStreamSite) + "?user_agent="+ str(user_agent) +"&wmsAuthSign=" + str(shash) + "/ch" + str(channel) + "q1.stream live=1 timeout=10"

##########################################################################
#            Routines used ONLY by MODE 997 (SportsAccess)               #
##########################################################################
def sa_url(url): 
    channel = url # determined earlier
    SportsAccessPassword    = selfAddon.getSetting('SportsAccessPassword')
    SportsAccessUserName    = selfAddon.getSetting('SportsAccessUserName')
    SportsAccessServer      = selfAddon.getSetting('SportsAccessServer')
    SportsAccessPort        = selfAddon.getSetting('SportsAccessPort')
    SportsAccessSite        = selfAddon.getSetting('SportsAccessSite')        
    SportsAccessURL         = selfAddon.getSetting('SportsAccessURL') 

    if SportsAccessServer == "0" :  SportsAccessServer = "eu.01.cdnstreams.in"  # Europe
    elif SportsAccessServer == "1": SportsAccessServer = "eu.02.cdnstreams.in"  # Europe 2
    elif SportsAccessServer == "2": SportsAccessServer = "usa.01.cdnstreams.in" # North East
    elif SportsAccessServer == "3": SportsAccessServer = "usa.02.cdnstreams.in" # North East 2  
    elif SportsAccessServer == "4": SportsAccessServer = "usa.03.cdnstreams.in" # West USA   
    elif SportsAccessServer == "5": SportsAccessServer = "usa.05.cdnstreams.in" # West Two   
    elif SportsAccessServer == "6": SportsAccessServer = "usa.06.cdnstreams.in" # South East  
    elif SportsAccessServer == "7": SportsAccessServer = "usa.07.cdnstreams.in" # South Central  
    elif SportsAccessServer == "8": SportsAccessServer = "usa.08.cdnstreams.in" # South Central  2 
    elif SportsAccessServer == "9": SportsAccessServer = "usa.09.cdnstreams.in" # Mid West/Central  
    elif SportsAccessServer == "10":SportsAccessServer = "usa.10.cdnstreams.in" # South East Two   
    data = {'username': SportsAccessUserName, 'password': SportsAccessPassword}   
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    response = opener.open(SportsAccessURL, data, 30)
    jsonRaw = response.read()
    opener.close()
    response.close()
    jsonObject = json.loads(jsonRaw)
    shash = jsonObject["hash"]
    return "http://"+SportsAccessServer+":"+SportsAccessPort+"/"+SportsAccessSite+"/ch"+channel+"q1/playlist.m3u8?wmsAuthSign="+shash

##########################################################################
#                     Routines only used by VADERStreams                 #
##########################################################################
def get_vader(url):
    VaderPassword = selfAddon.getSetting('VaderPassword')
    VaderUserName = selfAddon.getSetting('VaderUserName')       
    return "http://vaders.tv:80/live/"+str(VaderUserName)+"/"+str(VaderPassword)+"/"+str(url)+".ts"
   
##########################################################################
#                     Routines only used by USAIPTV                      #
##########################################################################
def get_usaiptv(url)   :
    USAIPTVToken = selfAddon.getSetting('USAIPTVToken')
    return "http://usaiptv.ddns.net:9090/load/"+str(USAIPTVToken)+"/"+url+".mpegts"
