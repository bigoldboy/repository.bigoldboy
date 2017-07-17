#############################################
#          Functions Library                #
#############################################
# from  bigoldboy import *
# version 0.1.2 developing

import xbmcgui, xbmc, sys, urllib, urllib2, xbmcplugin, xbmcvfs, datetime, time
from os.path import isfile, join
d   = xbmcgui.Dialog()
dp  = xbmcgui.DialogProgress()

################# prompts and displays ##################

# 1.1 Function to get input from keyboard
def get_input(what2say):
    x = d.input(what2say)
    return x

#1.2 function to troubleshoot on screen
def ts(what2say):
    xbmcgui.Dialog().notification("Troubleshooting",str(what2say),sound=False)        

#1.3 Display a page of text & can be very long
def takenote(what2say):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(500)
            retry -= 1
            win.getControl(1).setLabel("*** TAKE NOTE ***")
            win.getControl(5).setText(what2say)
            return
        except:
            pass

#1.4 Function to pop up a box with a message, and hit okay to continue
def attention(what2say):
    d.ok('ATTENTION!',what2say) 

#1.5 Function to create a progess box
def progress_create(title,what2say):
    dp.create(title,what2say)

#this function will just display something on the screen in small upper right box
# def information(what2say):
#     d.notification('INFORMATION SCREEN', what2say)


#this is defining a FUNCTION to write to the error log. Format is "logerror (error_text)"
#2.1 function to troubleshoot to log
def tl(what2say):
    xbmc.log(msg="------------------------> " + what2say)        

def out(what2say):
    mylog=xbmc.translatePath(join('special://logpath','ron.log'))
    f= open(mylog,"a+")
    f.write(str(what2say)+"\n")
    f.close

def outtime(what2say):
    out("--------------------------------------------------------")
    x=time.clock()
    try:
        mylog=xbmc.translatePath(join('special://logpath','ron.log'))
        f= open(mylog,"a+")
        f.write(datetime.datetime.now().strftime('%I:%M:%S %p')+": "+str(what2say)+"   Timer: "+str(x)+"\n")
        f.close
    except:
        
        pass


#################### Services ######################    

def addon_name():
    return sys.argv[0] 

def addon_number():
    return sys.argv[1]

def addon_parameters():
    return sys.argv[2] 

################# Files And Lists ##################

#this function will add a file to the directory list
def adddir(url, title, icon):
    addon_handle = int(sys.argv[1])
    li = xbmcgui.ListItem(title, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

#this function will open a file and return the contents after closing file


def readfile(filename):
    f    = xbmcvfs.File(filename, 'r')
    content = f.read()
    f.close()
    return content

# def readfile1(filename):  #no longer used - updated for smb: access
#     readfile = open(filename, 'r')
#     content = readfile.read()
#     readfile.close()
#     return content

# This function will open a URL online file 
def readurl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:19.0)  Chrome/45.0.2454.85 Safari/537.36 Gecko/20100101 Firefox/19.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link.replace('\n','').replace('\t','').replace('\r','')


# This function will add a directory item
def add_dir_item(handle="",folder='',mode='',url="",title='',iconimage='',fanart=''): #build my directory 
    if folder != '': 
        folder=True            
        if 'plugin://' in mode:  url=mode
        else: url = sys.argv[0]; url += "?url="+urllib.quote_plus(url);url += "&mode="+str(mode);url += "&title="+urllib.quote_plus(title);url += "&iconimage="+urllib.quote_plus(iconimage);url += "&fanart="+urllib.quote_plus(fanart)
    else:
        folder=False
    li = xbmcgui.ListItem(title, iconImage=iconimage)
    li.setInfo(type="Video", infoLabels={"Title": ""})
    li.setProperty("Fanart_Image",fanart)
    xbmcplugin.addDirectoryItem(handle=handle,url=url,listitem=li,isFolder=folder)    
    return



