from  bigoldboy import *
import re, xbmc, urllib2,  xbmcgui, xbmcplugin, datetime, os
from os.path import isfile, join
import gzip, json
from os.path import join
addon_handle = int(sys.argv[1])     
import codecs

#  code to read file line by line
# with open(filename) as f:
#     for line in f:
#         out(line)


def test():
    #readvader("2")
    downloadvaderm3u("2")
    #create_new_epg()
    return

def create_new_epg():
    ftvguide=xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ftvguide/settings.xml'))    
    thefile=readfile(ftvguide)
    x=thefile.find('xmltv.file" value="')    
    thefile=thefile[x+19:]
    x=thefile.find('" />')
    thefile=thefile[:x]
    joe =  xbmcvfs.exists(thefile)
    if joe == 1: 
        ts("SAMMY")
    else: 
         ts("NO")
    #f =xbmcvfs.File (thefile, 'rw', True)

    vfsfile = xbmcvfs.File(thefile)
    size = vfsfile.size()

    
    # # this routine will delete the old data, and update to the new data
    # reset_hdhomerun() #also, bonus, reset HDHomerun to 3.1 as sometimes it won't boot if on week station    
    # vaderxmltv="C:\Users\\rondyer\Dropbox\kodibox\portable_data\userdata\\addon_data/plugin.video.VADER/VADER_xmltv.xml.gz"
    # #make sure it is there, if not just exit
    # ftvpath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.ftvguide/'))    
    # xbmcvfs.delete(ftvpath+"ftvguide.ini")
    # xbmcvfs.delete(ftvpath+"source.db")
    # xbmcvfs.delete(ftvpath+"XLMTVNEWVADERPLUS.xml")
    
    
    # if os.path.isfile(vaderxmltv):
        
    #     progress_create("Creating EPG",str.center("Opening Vader .gz EPG ",114,' '))                               
    #     with gzip.open(vaderxmltv, 'rb') as f: completexmltv = f.read()  #open and read it
    #     time.sleep(1)    

    #     # open the file to write our new xmltv to
    #     file2write="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XLMTVNEWVADERPLUS.xml"
    #     os.remove(file2write)#delete first
    #     f=open(file2write,"a+")

    #     # copy XMLTV Header from file (has all the channel info)
    #     headerfile="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\VADERHEADER.xml"
    #     contents=readfile(headerfile)  #open the main menu
    #     f.write(contents)

    #     # pull the channels out of header file to search the vader epg for 
    #     mychannels=re.compile('<channel id="(.+?)">').findall(contents);x=0        
    #     for thischannel in mychannels: # have a list of my channels  
    #         x=x+1   
    #         progress_create("Creating EPG",str.center("Reading & Writing Channel: "+str(x),120-len(thischannel),' '))               
    #         contents=completexmltv  #restore full epg
    #         contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up             
    #         contents = re.compile('<programme channel="(.+?)</programme>').findall(contents)        
    #         for listing in contents:
    #             if thischannel in listing: f.write('<programme channel="'+listing+'</programme>\n\n')                        

    #     # add ron's special epg
    #     ronxmltv="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XMLTVNEW.xml"
    #     progress_create("Creating EPG",str.center("Adding Ron's EPG Now... ",114,' '));time.sleep(1)
    #     contents=readfile(ronxmltv) #read in Ron's EPG
    #     x=contents.find('webgrabplus.com">')  
    #     contents=contents[x+18:]#remove header    
    #     f.write(contents)
    #     f.close #close the new XMLTV file
    #     ts("All Done!")
    # else:
    #     ts("Didn't find the EPG file to work from")
    sys.exit() 




def tiki():
    tikipage="http://www.tikilive.com/radios/#filter/alphaaz"     
    contents = urllib2.urlopen(tikipage).read() 
    out(contents)     
    x=contents.find('<div class="btn-group z-index-1 margin-left-small">');contents=contents[x:]
    y=contents.find('<ul class="dropdown-menu" id="channels_filter">');contents=contents[:y]
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile('featured_radios">(.+?)</a>').findall(contents)   
    for stationinfo in contents:
        stationinfo=stationinfo[4:]          
        if'"' in stationinfo or len(stationinfo) < 3 : pass
        else: add_dir_item(handle=addon_handle,folder="",mode="",url="url",title="[COLOR red]Tiki [COLOR white]"+stationinfo+"[/COLOR]",iconimage="x")         
    

def yusa1(): # June 21 Yesterday USA
    yusaschedule="http://www.yesterdayusa.com/cgi-bin/schedule4.pl" ;x=0
    contents = urllib2.urlopen(yusaschedule).read()      
    out("\n88888888888 total dump 88888888888888")
    out(contents)
    out("88888888888 END DUMP 88888888888888\n\n")
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile('<font face="Georgia" size="2">(.+?)</font>').findall(contents)    
    for proglisting in contents:            
        x=x+1
        if x==1: 
            y=proglisting.find("<br>");title=proglisting[:y]
            url="https://streaming.radio.co/sf5708c004/listen" #red
            url="plugin://plugin.video.bobtv/?url="+url+"&name=radiostation YUSA RED: "+title+"&mode=1000&extra=https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg"
            add_dir_item(handle=addon_handle,folder="",mode="",url=url,title="[COLOR red]RED: [COLOR white]"+title+"[/COLOR]",iconimage="https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg")

        elif x==2:
            y=proglisting.find("<br>");title=proglisting[:y]
            url="https://streaming.radio.co/sa37b728bf/listen" #blue
            url="plugin://plugin.video.bobtv/?url="+url+"&name=radiostation&mode=1000&extra=https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg"
            add_dir_item(handle=addon_handle,folder="",mode="",url=url,title="[COLOR blue]BLUE: [COLOR white]"+title+"[/COLOR]",iconimage="https://i3.radionomy.com/radios/400/c571e51d-a8a7-490d-997a-d431a332936d.jpg")

        else:
            y=proglisting.find(" on ")         
            out("Next: "+proglisting[:y])
            programinfo = re.compile('<font face="Georgia" size="2">(.+?)<br></td>.+?<font face="Georgia" size="2">(.+?)<br></td>').findall(proglisting)
            for nothing,redshow in programinfo:
                out("redshow: "+redshow)            
        



def readbook():
    myfile="C:\Users\\rondyer\Dropbox\kodibox\portable_data\\book2.txt"
    contents=readfile(myfile)
    contents = re.compile(':RON:(.+?))  ').findall(contents)
    out(str(contents))
    
def radiotunes():
    rawrt="https://www.radiotunes.com/" 
    rawrt="https://www.radiotunes.com/lovemusic" 
    contents = urllib2.urlopen(rawrt).read()      
    out(contents)
    #contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    # contents = re.compile('{"ad_channels":(.+?)}.').findall(contents)
    # for stationinfo in contents:            
    #     out("\n"+stationinfo)
    


def downloadvaderm3u(channelnumber):    
    contents = urllib2.urlopen("http://vaders.tv/panel_api.php?username=rondyer@gmail.com&password=rondyer").read()
    data = json.loads(contents) #Makes it json data    
    for channel in data:
        out(data[channel])
    
    # contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    # contents = re.compile('name="(.+?)" .+?group-title="(.+?)",.+?rondyer/(.+?).ts').findall(contents)
    # for stationname,group,url in contents:            
    #         if channelnumber == url: return stationname
    # return "No Station Name"
    



def wwtk():  #Working on Walk With The King to play episodes on demand  June 1 2017
    vaderplaylist="http://www.walkwiththeking.org/force-download-audio.php" 
    out(vaderplaylist)
    contents = urllib2.urlopen(vaderplaylist).read()
    out(str(contents))
    # contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    # contents = re.compile("<plugin>(.+?)</plugin>").findall(contents)
    # for entry in contents:        
    #         joe = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(entry)
    #         for title,url,fanart in joe:
    #             out("<item> <title>[COLOR white]"+title+"[/COLOR]</title>")
    #             out("<url>folder "+url+"</url>")
    #             out("<thumbnail>"+fanart+"</thumbnail>")
    #             out("<fanart>"+fanart+"</fanart></item>\n")
    # return


def readchannelnames(): #reads the Vader EPG data from .gz file and lists them
    vaderxmltv="C:\Users\\rondyer\Dropbox\kodibox\portable_data\userdata\\addon_data/plugin.video.VADER/VADER_xmltv.xml.gz"
    with gzip.open(vaderxmltv, 'rb') as f: contents = f.read()    
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up  
    contents=re.compile('<channel(.+?)"><d.+?-name>(.+?)</display-name>').findall(contents) #parse               
    for number,name in contents:
        out(name)
    
def combinexmltv(): # combine 2 files into one XMLTV
    vaderxmltv="C:\Users\\rondyer\Dropbox\kodibox\portable_data\userdata\\addon_data/plugin.video.VADER/VADER_xmltv.xml.gz"
    with gzip.open(vaderxmltv, 'rb') as f: firstpart = f.read()    # read in the Vader EPG    
    x=firstpart.find("</tv>"); firstpart=firstpart[:x]  #remove the bottom of it ("</tv>")    
    ronxmltv="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XMLTVNEW.xml"
    secondpart=readfile(ronxmltv) #read in Ron's EPG
    x=secondpart.find('webgrabplus.com">')  ;secondpart=secondpart[x+18:]#remove header    
    newxml=firstpart+secondpart #merge together    
    combined="C:\Users\\rondyer\Dropbox\KodiSupport\TV Guide XML\XMLTVNEWCOM.xml"
    f=open(combined,"w") ;f.write(newxml); f.close #write the file    

    
def readvader(whichtype):  #This routine reads vader streams and formats the way i like
    vaderfile="C:\Users\\rondyer\Dropbox\kodibox\portable_data\userdata\\addon_data\plugin.video.VADER\get_vod_streams"    
    contents=readfile(vaderfile)    
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up        
    contents=re.compile('name":"(.+?)",".+?type":"(.+?)",".+?category_id":"(.+?)",".+?series_no":(.+?),"c').findall(contents) #parse         
    #for vnum,name,typeof,url,icon,dateadded,catagory,seriesnum,contain,custsid,direct in contents:
    for name,typeof,catagory,seriesnum in contents:
        #out(name+"\t"+typeof+"\t"+url+"\t"+icon+"\t"+dateadded+"\t"+catagory+"\t"+seriesnum+"\t"+contain+"\t"+custsid+"\t"+direct)
        out(name+"\t"+typeof+"\t"+catagory+"\t"+seriesnum)
        #str(datetime.datetime.fromtimestamp(int(dateadded)))
#        if vnum == "200": break


    # for title,typeof,channum in sorted(contents):
    #     if "- S1" in title or "- S0" in title or "- 2017" in title: typeof="tvshow"
    #     if whichtype == "live":
    #         if typeof == "live":
    #             vurl="plugin://plugin.video.bobtv/?url="+channum[0:-3]+"&name="+title+"&mode=990&title=Live Stream"
    #             vtitle="[COLOR lightgreen]"+str(title)+"[COLOR yellow] ("+str(channum[0:-3])+")[/COLOR]"
    #             add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                       
    #     elif whichtype == "movie":
    #         if typeof == "movie":
    #             url=  "http://vaders.tv/movie/rondyer@gmail.com/rondyer/"+channum
    #             vurl="plugin://plugin.video.bobtv/?url="+url+"&name=Vader Movie&mode=1000&title="+title                
    #             vtitle="[COLOR lightgreen]"+str(title)+"[/COLOR]"
    #             add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                                       
    #     elif whichtype == "tvshow":
    #         if typeof == "tvshow":
    #             url=  "http://vaders.tv/movie/rondyer@gmail.com/rondyer/"+channum
    #             vurl="plugin://plugin.video.bobtv/?url="+url+"&name=Vader TV Show&mode=1000&title="+title                
    #             vtitle="[COLOR lightgreen]"+str(title)+"[/COLOR]"
    #             add_dir_item(handle=addon_handle,folder="",mode="",url=str(vurl),title=str(vtitle),iconimage="http://orig02.deviantart.net/117c/f/2016/090/8/a/darth_vader_thumbs_up_opt_by_zacmariozero-d9x8htv.jpg",fanart="https://seo-michael.co.uk/content/images/2016/02/vaderfeat.jpg")                                       
    #     else: ts("Unknown Category")


def read_all_vader_channels():
    #find the vader m3u list
    #open it and compare to the channel number given
    #if match retrurn name
    return

def trywalk():
    import os

    for root, dirs, files in os.walk("d:\onedrive\\", topdown=False):
        for name in files:
            out(str(os.path.join(root, name)))
        for name in dirs:
            out(str(os.path.join(root, name)))


def smoothlist():  #Loads favs from Kodi Radio App
    radiofile = xbmc.translatePath(join('special://userdata', 'addon_data', 'script.smoothstreams', 'SmoothStreams.json'))
    contents=readfile(radiofile)    
    out(contents)
    contents=contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up

    # contents= re.compile('"name":"(.+?)".+?"thumbnail":"(.+?)".+?stream_url":"(.+?)"').findall(contents) #parse 
    # imageicon="http://kodi.dvwd.net/sites/default/files/styles/medium_crop/public/addon/field_image/icon_432.png?itok=6rrhtcDk"
    # fanart="http://kodi.dvwd.net/sites/default/files/styles/medium_crop/public/addon/field_image/icon_432.png?itok=6rrhtcDk"
    # for title,mythumb,url in contents: 
    #     title="[COLOR yellow]Kodi Radio: [COLOR red]"+title+"[/COLOR]"
    #     add_dir_item(handle=addon_handle,folder="",mode="",url=str(url),title=str(title),iconimage=mythumb,fanart=mythumb)                



def one242list(): # wrote this to search multichannels for vader catchup
    vaderplaylist="http://one242415.offshorepastebin.com/RETRO/50s.xml" 
    contents = urllib2.urlopen(vaderplaylist).read()
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile("<plugin>(.+?)</plugin>").findall(contents)
    for entry in contents:        
            joe = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(entry)
            for title,url,fanart in joe:
                out("<item> <title>[COLOR white]"+title+"[/COLOR]</title>")
                out("<url>folder "+url+"</url>")
                out("<thumbnail>"+fanart+"</thumbnail>")
                out("<fanart>"+fanart+"</fanart></item>\n")
    return

# May 7 2017 routine to read file at one242415 that are YOUTUBE and create output to go into one of my bobcollection xml files
def one242list4youtube(): # wrote this to search multichannels for vader catchup
    vaderplaylist="http://one242415.offshorepastebin.com/RETRO/2000s.xml" 
    contents = urllib2.urlopen(vaderplaylist).read()
    contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
    contents = re.compile("<plugin>(.+?)</plugin>").findall(contents)
    for entry in contents:        
            joe = re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>').findall(entry)
            for title,url,fanart in joe:
                out("<item> <title>[COLOR white]"+title+"[/COLOR]</title>")
                out("<url>folder "+url+"</url>")
                out("<thumbnail>"+fanart+"</thumbnail>")
                out("<fanart>"+fanart+"</fanart></item>\n")
    return


# May 4 2017 create a file and write to it 
def loadurltofile(url):	
	xferfile= xbmc.translatePath(join('special://logpath','vaderxfer'))
    	f=open(xferfile,"a+")
    	f.write(url)
    	f.close
    	
#May 18 routine to read Vader m3u list and return the channel name based on number
def vaderlist(channelnumber): # wrote this to search multichannels for vader catchup
	vaderplaylist="http://api.vaders.tv/vget?username=rondyer@gmail.com&password=rondyer&format=ts"	
	contents = urllib2.urlopen(vaderplaylist).read()
	contents = contents.replace('\t',"").replace('\n',"").replace('\r','') # clean it up 
	contents = re.compile('name="(.+?)" .+?group-title="(.+?)",.+?rondyer/(.+?).ts').findall(contents)
	for stationname,group,url in contents:
            if channelnumber in url: return stationname
            else: return "No Station Name"


def outer(what2say):
    try:
        f= open("ron.log","a+")
        f.write(str(what2say)+"\n")
        f.close
    except:
        
        pass

def test_read_url(urlname):
	return unicode(urllib2.urlopen(urlname).read(),'utf-8')
	return readurl(urlname)

def read_seinfeld(addon_handle):  # gives us daily seinfeld
    html = urllib2.urlopen('http://www.jerryseinfeld.com/').read()    
    for v in re.finditer('"title":"(.+?)","filename":"(.+?)"' + ',"appearance":"(.+?)","venue":"(.+?)"', html):
        title, filename, year, venue = v.groups()
        li = xbmcgui.ListItem('[COLOR white]('+year+') [COLOR yellow]'+title+"[/COLOR]"  , iconImage='http://static.tumblr.com/oog0lak/icgl5id5u/fbdf.png',thumbnailImage="http://static.tumblr.com/oog0lak/icgl5id5u/fbdf.png")
        li.setInfo(type="Video", infoLabels={"mediatype": "movie","Title":'[COLOR white]'+title+'[/COLOR]', "studio": '[COLOR yellow]'+str(year)+' - '+venue+'[/COLOR]' })
        li.setProperty("Fanart_Image",'http://matemedia.com/wp-content/uploads/2015/04/JerrySeinfeld-trans-300x229.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle,url='http://cdn.jerryseinfeld.com/assets'+"/"+str(filename)+".mp4",listitem=li)
    
def grabhtml():	
	url2get="http://www.cbc.ca/archives/entry/big-city-blues-toronto-becoming-a-victim-of-its-own-success"
	out("\n\n============== contents of "+url2get+" ================")
   	out(test_read_url(url2get))
   	out("============== end of "+url2get+" ================\n\n")    