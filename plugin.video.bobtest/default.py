import xbmc, xbmcgui, xbmcplugin, xbmcaddon 
import os, sys, urllib, re, urlparse, urllib2, datetime, json, xbmcvfs, gzip
from  bigoldboy import *
from resources.lib import seinfeld
from resources.lib import playground
from os.path import join

addon = xbmcaddon.Addon()
addon_url = sys.argv[0]                   # Get the plugin url (plugin://plugin.video.bobcollection/)
addon_handle = int(sys.argv[1])           # Get the plugin handle as an integer number. (interger)
addon_name = addon.getAddonInfo('name')   # Get the addon name (bobcollection)
addon_id = addon.getAddonInfo('id')       # Get the addon id (plugin.video.bobcollection)
addon_path = addon.getAddonInfo('path')   # C:\Users\rondyer\Dropbox\Kodibox\portable_data\addons\plugin.video.bobcollection
where_r_files=addon.getSetting("where_r_files")
##############################################################################################
addon_handle = int(sys.argv[1])           # Create the directory structure
##############################################################################################
def run(): #Main program which loads up main menu
    if mode   == None:                  CreateMenu(where_r_files+'1mainmenu.xml')
    elif "ActivateWindow" in mode :     window(mode)
    elif mode == "otanews":             otafiles(addon.getSetting("otanews"))
    elif mode == "otashows":            otafiles(addon.getSetting("otashows"))
    elif mode == "livesongs":           otafiles(addon.getSetting("livesongs"))
    elif mode == "seinfeld":            seinfeld.daily_seinfeld(addon_handle)    
    elif mode == "test":                playground.test()
    elif mode == "SmoothStreams":       xbmc.executebuiltin('RunScript(script.smoothstreams)');sys.exit()        
    elif mode == "MatchCentre":         xbmc.executebuiltin('XBMC.RunPlugin(%s)' % 'plugin://plugin.video.VADER/mc/');sys.exit()  
    elif mode == "BobGuide":            bobguide()
    elif mode == "CreateEPG":           create_new_epg()
    elif mode == "vaderlistlive":       vaderList("live")
    elif mode == "vaderlistmovie":      vaderList("movie")
    elif mode == "vaderlisttvshow":     vaderList("tvshow")  
    elif mode == "all181fm":            all181fm()  
    elif mode == "yusa":                yusa()      
    else:                               CreateMenu(where_r_files+str(mode)+'.xml')

def window(whichwin):
    xbmc.executebuiltin(whichwin)

def yusa(): # June 21 Yesterday USA
    yusaschedule="http://www.yesterdayusa.com/cgi-bin/schedule4.pl" ;x=0
    contents = urllib2.urlopen(yusaschedule).read()      
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile('<font face="Georgia" size="2">(.+?)</font>').findall(contents)    
    for proglisting in contents:            
        x=x+1
        if x==1: #Red stream
            y=proglisting.find("<br>");title=proglisting[:y]
            url="https://streaming.radio.co/sf5708c004/listen" #red
            url="plugin://plugin.video.bobtv/?url="+url+"&name=radiostation YUSA RED: "+title+"&mode=1000&extra=https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg"
            add_dir_item(handle=addon_handle,folder="",mode="",url=url,title="[COLOR red]RED: [COLOR white]"+title+"[/COLOR]",iconimage="https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg")

        elif x==2: #Blue Steram
            y=proglisting.find("<br>");title=proglisting[:y]
            url="https://streaming.radio.co/sa37b728bf/listen" #blue
            url="plugin://plugin.video.bobtv/?url="+url+"&name=radiostation YUSA BLUE: "+title+"&mode=1000&extra=https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg"
            add_dir_item(handle=addon_handle,folder="",mode="",url=url,title="[COLOR blue]BLUE: [COLOR white]"+title+"[/COLOR]",iconimage="https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg")

def all181fm():  # This will interrogate the 181.fm web and return list of stations and links
    contents = urllib2.urlopen("http://www.181.fm/index.php?p=mp3links").read()      
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile('<tr>(.+?)</tr>').findall(contents)
    for stationname in contents:
        contents = re.compile('<td align="left" id="rightlinks">(.+?)</td>.+?<a href="(.+?)">128k').findall(stationname)            
        for name,link in contents:
            url=link.replace("&","$").replace("=","~")
            url="plugin://plugin.video.bobtv/?url="+url+"&name=radiostation&mode=1000&extra=http://www.181.fm/images/playerlanding/181.FM.jpg"
            add_dir_item(handle=addon_handle,folder="",mode="",url=url,title="[COLOR red]181.fm [COLOR white]"
            +name+"[/COLOR]",iconimage="http://www.181.fm/images/playerlanding/181.FM.jpg",fanart="http://3.bp.blogspot.com/-fMk_kV8-KRw/TlEoBF6L1NI/AAAAAAAAB58/ryL48ChfeOI/s1600/181logo.png")

def reset_hdhomerun():
    hdhomerun=xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.hdhomerun.view/settings.xml'))    
    thefile=readfile(hdhomerun)
    x=thefile.find('<setting id="last.channel"');first=thefile[:x]
    y=thefile.find('<setting id="overlay.timeout"');second=thefile[y:]
    newfile=first+'<setting id="last.channel" value="3.1" />\n\t'+second
    f=open(hdhomerun,"w")
    f.write(newfile)
    f.close
    
def create_new_epg():
    # this routine will delete the old data, and update to the new data
    reset_hdhomerun() #also, bonus, reset HDHomerun to 3.1 as sometimes it won't boot if on week station    
    vaderxmltv="C:\Users\\rondyer\Dropbox\kodibox\portable_data\userdata\\addon_data/plugin.video.VADER/VADER_xmltv.xml.gz"
    #make sure it is there, if not just exit
    ftvpath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ftvguide/'))    
    xbmcvfs.delete(ftvpath+"ftvguide.ini")
    xbmcvfs.delete(ftvpath+"source.db")
    xbmcvfs.delete(ftvpath+"XLMTVNEWVADERPLUS.xml")
    
    
    if os.path.isfile(vaderxmltv):
        
        progress_create("Creating EPG",str.center("Opening Vader .gz EPG ",114,' '))                               
        with gzip.open(vaderxmltv, 'rb') as f: completexmltv = f.read()  #open and read it
        time.sleep(1)    

        # open the file to write our new xmltv to
        file2write="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XLMTVNEWVADERPLUS.xml"
        os.remove(file2write)#delete first
        f=open(file2write,"a+")

        # copy XMLTV Header from file (has all the channel info)
        headerfile="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\VADERHEADER.xml"
        contents=readfile(headerfile)  #open the main menu
        f.write(contents)

        # pull the channels out of header file to search the vader epg for 
        mychannels=re.compile('<channel id="(.+?)">').findall(contents);x=0        
        for thischannel in mychannels: # have a list of my channels  
            x=x+1   
            progress_create("Creating EPG",str.center("Reading & Writing Channel: "+str(x),120-len(thischannel),' '))               
            contents=completexmltv  #restore full epg
            contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up             
            contents = re.compile('<programme channel="(.+?)</programme>').findall(contents)        
            for listing in contents:
                if thischannel in listing: f.write('<programme channel="'+listing+'</programme>\n\n')                        

        # add ron's special epg
        ronxmltv="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XMLTVNEW.xml"
        progress_create("Creating EPG",str.center("Adding Ron's EPG Now... ",114,' '));time.sleep(1)
        contents=readfile(ronxmltv) #read in Ron's EPG
        x=contents.find('webgrabplus.com">')  
        contents=contents[x+18:]#remove header    
        f.write(contents)
        f.close #close the new XMLTV file
        ts("All Done!")
    else:
        ts("Didn't find the EPG file to work from")
    sys.exit() 

   
def bobguide():    
    xbmc.executebuiltin('RunScript(script.tvguide.fullscreen)');sys.exit()        

def tvguide():
    xbmc.executebuiltin('RunScript(script.tvguide)');sys.exit()        

def CreateMenu(which_file):   #Load from a XML file into directory
    xbmcplugin.setContent(addon_handle, 'videos')
    if 'http' in which_file:  contents=readurl(which_file)
    else: contents=readfile(which_file)  #open the main menu
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents= re.compile('<item>(.+?)</item>').findall(contents) #parse 
    for item in contents: #Read 4 items then load up into a menu
            data=re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)            
            for title,url,iconimage,fanart in data:
                if 'folder' in url: # if folder then parse second part and make it the url                    
                    x=url.find(" ") ; mode=url[x+1:]
                    add_dir_item(handle=addon_handle,folder="folder",mode=mode,url=str(url),title=str(title),iconimage=iconimage,fanart=fanart)
                else:
                    mode=url
                    add_dir_item(handle=addon_handle,folder=""      ,mode=mode,url=str(url),title=str(title),iconimage=iconimage,fanart=fanart)
                
    if "radio.xml" in which_file >0 : #if this is radio, also load from two other sources)
        addradio = addon.getSetting("addradio") 
        if addradio=="true": kodiradio()
        addtapin = addon.getSetting("addtapin") 
        if addtapin=="true": 
            tapinradio()    
   
# --------------------------------- Routines --------------------------------------
def otafiles(mypath):  # Loads in local OTA .TS files - uses otaname
    from os.path import join
    top_dirs, top_files = xbmcvfs.listdir(mypath)
    for thisdir in top_dirs: # start at the top level and start drilling down                
        second_dirs, second_files=xbmcvfs.listdir(mypath+thisdir) #get list of dirs and files
        for filedir in second_dirs:
            third_dirs, third_files=xbmcvfs.listdir(mypath+thisdir+"/"+filedir) #get list of dirs and files
            for filename in third_files:                
                #if filename[len(filename)-3:] == ".ts" and "Episode" in filename :                    
                if filename[len(filename)-3:] == ".ts" :                    
                    url = os.path.join(mypath, thisdir,filedir,filename)                                   
                    add_dir_item(handle=addon_handle,folder='',mode='',url=url,title=otaname(filename),iconimage='x',fanart='x')

def otaname(filename): # Creates the Display name based upon the local file name. Called by OTAFILES    
    if ".ts" in filename:                            
        if "Episode" in filename:  #NEWS  
            x=filename.find("("); first=filename[:x-1];information=filename[x+9:];year=information[0:4];month=information[5:7]
            day=information[8:10];t = datetime.datetime(int(year),int(month),int(day));second = t.strftime('%A, %B %d')
            return "[COLOR lightgreen]" + first + "  -  [COLOR red]" + second + "[/COLOR]"
        elif ") - S" in filename: #SERIES            
            x=filename.find(" - ")
            first=filename[:x-7]
            episode=filename[x+3:x+10]
            epititle=filename[x+11:-3]
            return "[COLOR lightgreen]" + first + " [COLOR red](" + episode + ")[COLOR lightblue]" + epititle +"[/COLOR]"
        else: return filename
    return filename

def kodiradio():  #Loads favs from Kodi Radio App
    radiofile = xbmc.translatePath(join('special://userdata', 'addon_data', 'plugin.audio.radio_de', '.storage', 'my_stations.json'))
    contents=readfile(radiofile)    
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up
    contents= re.compile('"name":"(.+?)".+?"thumbnail":"(.+?)".+?stream_url":"(.+?)"').findall(contents) #parse 
    imageicon="http://kodi.dvwd.net/sites/default/files/styles/medium_crop/public/addon/field_image/icon_432.png?itok=6rrhtcDk"
    fanart="http://kodi.dvwd.net/sites/default/files/styles/medium_crop/public/addon/field_image/icon_432.png?itok=6rrhtcDk"
    for title,mythumb,url in contents: 
        title="[COLOR yellow]Kodi Radio: [COLOR red]"+title+"[/COLOR]"
        add_dir_item(handle=addon_handle,folder="",mode="",url=str(url),title=str(title),iconimage=mythumb,fanart=mythumb)                
    
def tapinradio(): #Loads favs from Tapin Fav file
    try:
        tapinfile=addon.getSetting("tapinfavs")
        contents=readfile(tapinfile)
        contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up
        contents= re.compile('<Station title="(.+?)".+?<Source>(.+?)</Source>').findall(contents) #parse 
        imageicon="https://pbs.twimg.com/profile_images/1535023540/main_large_400x400.png"
        fanart="http://1.bp.blogspot.com/-nw3YgpUn2WE/Vm31oNtfzdI/AAAAAAAAAuQ/if6MB85N7og/s1600/TapinRadio%2BPro.jpg"
        for title,url in contents: 
            title="[COLOR yellow]Tapin: [COLOR cyan]"+title+"[/COLOR]"
            add_dir_item(handle=addon_handle,folder="",mode="",url=str(url),title=str(title),iconimage=imageicon,fanart=fanart)                
    except:
        pass
            
def vaderList(whichtype):
    vaderfile="http://vaders.tv/get.php?username=rondyer@gmail.com&password=rondyer&type=m3u&output=ts"    
    contents=readfile(vaderfile)    
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up        
    contents= re.compile('-1,(.+?)http://.+?.tv/(.+?)/ron.+?rondyer/(.+?)#').findall(contents) #parse         
    for title,typeof,channum in sorted(contents):
        if "- S1" in title or "- S0" in title or "- 2017" in title: typeof="tvshow"
        if whichtype == "live":
            if typeof == "live":
                vurl="plugin://plugin.video.bobtv/?url="+channum[0:-3]+"&name="+title+"&mode=990&title=Live Stream"
                vtitle="[COLOR lightgreen]"+str(title)+"[COLOR yellow] ("+str(channum[0:-3])+")[/COLOR]"
                add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                       
        elif whichtype == "movie":
            if typeof == "movie":
                url=  "http://vaders.tv/movie/rondyer@gmail.com/rondyer/"+channum
                vurl="plugin://plugin.video.bobtv/?url="+url+"&name=Vader Movie&mode=1000&title="+title                
                vtitle="[COLOR lightgreen]"+str(title)+"[/COLOR]"
                add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                                       
        elif whichtype == "tvshow":
            if typeof == "tvshow":
                url=  "http://vaders.tv/movie/rondyer@gmail.com/rondyer/"+channum
                vurl="plugin://plugin.video.bobtv/?url="+url+"&name=Vader TV Show&mode=1000&title="+title                
                vtitle="[COLOR lightgreen]"+str(title)+"[/COLOR]"
                add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                                       
        else: ts("Unknown Category")

    
def get_params(): # What parameters have been passed?   
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:  # see if we have anything. first char is ? 
        params = sys.argv[2][1:]   # load string passed into var params
        cleanedparams = params.replace('', '')  # clean up the params 
        if (params[len(params) - 1] == '/'):    #remove trailing slash
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        sammy=range(len(pairsofparams))
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]    
    return param
#############################################################################
# 							Start of Bob Collection 						#
#############################################################################
params = get_params(); url=""; name=None; mode=None; iconimage=None;progtitle=None;extra=""
#ts("New Run")
try: url = urllib.unquote_plus(params["url"]) 
except: pass
url = url.replace("~","=")  # if url has an equal sign in it, it was changed to'~' so change it back

try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode=urllib.unquote_plus(params["mode"])
except: pass
try: progtitle = urllib.unquote_plus(params["title"])
except: pass
try: extra = urllib.unquote_plus(params["extra"])
except: pass

run()
xbmcplugin.endOfDirectory(addon_handle)



