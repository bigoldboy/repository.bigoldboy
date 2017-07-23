import xbmcgui
import xbmc
import plugintools
import traceback
import urllib2
import json
import time
from datetime import datetime
import utils
import kodigui
import hashlib
import subprocess
import os
import xbmcaddon
import requests
import vader

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
ADDONNAME = __addon__.getAddonInfo('name')
ADDONID = __addon__.getAddonInfo('id')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')


LOGPATH  = xbmc.translatePath('special://logpath')
DATABASEPATH = xbmc.translatePath('special://database')
USERDATAPATH = xbmc.translatePath('special://userdata')
ADDONDATA = xbmc.translatePath( __addon__.getAddonInfo('profile') )
PVRADDONDATA = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/pvr.iptvsimple')
THUMBPATH = xbmc.translatePath('special://thumbnails')
ADDONLIBPATH = os.path.join(xbmcaddon.Addon(ADDONID).getAddonInfo('path'), 'lib')
ADDONPATH = xbmcaddon.Addon(ADDONID).getAddonInfo('path')
KODIPATH = xbmc.translatePath('special://xbmc')



class BaseDialog(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self._closing = False
        self._winID = ''

    def onInit(self):
        self._winID = xbmcgui.getCurrentWindowDialogId()

    def setProperty(self,key,value):
        if self._closing: return
        xbmcgui.Window(self._winID).setProperty(key,value)
        xbmcgui.WindowXMLDialog.setProperty(self,key,value)

    def doClose(self):
        self._closing = True
        self.close()

    def onClosed(self): pass

class BaseWindow(xbmcgui.WindowXML):
    def __init__(self,*args,**kwargs):
        self._closing = False
        self._winID = ''

    def onInit(self):
        self._winID = xbmcgui.getCurrentWindowId()

    def setProperty(self,key,value):
        if self._closing: return
        xbmcgui.Window(self._winID).setProperty(key,value)
        xbmcgui.WindowXMLDialog.setProperty(self,key,value)

    def doClose(self):
        self._closing = True
        self.close()

    def onClosed(self): pass

class MyAddon(BaseWindow):
    def __init__(self,*args,**kwargs):
        """Class constructor"""
        # Call the base class' constructor.
        self.player = xbmc.Player()
        self.eventMap = {}
        self.mcData = None
        self.vader = vader.vader()
        BaseWindow.__init__(self,*args,**kwargs)



    def createVersionSelect(self, item):
        d = utils.xbmcDialogSelect()
        versions = item.versions
        for version in versions:
            d.addItem(version['stream'], version['name'])

        selection = d.getResult()
        if selection:
           self.playfromStream(selection)

    def onClick(self,controlID):
        if controlID == 101:
            self.categorySelected()
        elif controlID == 201:
            self.programSelected()

    def onAction(self, action):


        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            # xbmc.executebuiltin("RunPlugin(plugin://plugin.video.VADER/menu)")
            plugintools.set_setting('mcClosedTime', str(int(time.time())))

            self.close()

        #return True


    def onInit(self):
        self.programsList = kodigui.ManagedControlList(self,201,11)
        self.categoryList = self.getControl(101)
        self.catList = []
        try:
            self.mcList()
        except:
            utils.log(traceback.format_exc())
            pass
        try:
            self.fillCategories()
        except:
            utils.log(traceback.format_exc())
            pass


    def fillCategories(self):
        items = []
        item = xbmcgui.ListItem('All')
        # item.setProperty('color', utils.makeColorGif('FFFFFFFF',os.path.join(utils.COLOR_GIF_PATH,'{0}.gif'.format('FFFFFFFF'))))
        items.append(item)

        for epgItem in self.mcData:

            itemCategory = epgItem['category']


            if itemCategory not in self.catList:
                self.catList.append(itemCategory)

        self.catList.sort()
        for c in self.catList:
            if c != '':
                item = xbmcgui.ListItem(c)
                item.setProperty('category',c.strip('- '))
                # item.setProperty('color',self.getGifPath(c))
                items.append(item)
        self.categoryList.reset()
        self.categoryList.addItems(items)


    def playfromStream(self,stream):

        apiEndpoint = self.vader.apiEndpoint
        username = self.vader.username
        password = self.vader.password
        embedded = self.vader.embedded

        if embedded == True:

            apkPath = os.path.abspath(os.path.join(KODIPATH, os.pardir))
            cachePath = os.path.abspath(os.path.join(apkPath, os.pardir))
            mainPath = os.path.abspath(os.path.join(cachePath, os.pardir))

            neededPath = mainPath + '/code_cache/a.out'

            p = subprocess.Popen([neededPath], stdout=subprocess.PIPE)
            out, err = p.communicate()
            username = out.split(':')[0].strip()
            password = out.split(':')[1].strip()


            timeNow = time.time()
            diffTime = timeNow % 3600
            tokenTime = timeNow - diffTime
            base = 'live'
            extension = 'ts'
            tokenString = username + password + str(stream) + str(tokenTime)
            token = hashlib.md5(tokenString).hexdigest()

            chanUrl = 'http://{apiEndpoint/boxRedir?token={token}&stream={stream}&base={base}&extension={extension}&plugin={plugin}'.format(
                token=token,
                stream=stream,
                base=base,
                extension=extension,
                plugin=ADDONID,
                apiEndpoint=apiEndpoint)
            self.player.play(chanUrl)

        else:
            chanUrl = 'http://%s/live/%s/%s/%s.%s' % (apiEndpoint,username, password, stream, 'ts')
            self.player.play(chanUrl)

    def categorySelected(self):
        item = self.categoryList.getSelectedItem()
        if not item:
            return
        cat = item.getProperty('category')
        if not cat:
            self.category = None
        else:
            self.category = cat
        # self.setProperty('category',item.getLabel().strip('- '))
        plugintools.set_setting('mcLastCategory', cat)
        self.showPrograms(cat)

    def showPrograms(self, cat):

        self.setFocusId(201)
        self.mcList(category=cat)

    def programSelected(self):
        item = self.programsList.getSelectedItem()
        if not item:
            return

        if item.versions == None:
            self.playFromEvent(item)

        else:
            self.createVersionSelect(item)

    def playFromEvent(self,item):
        url = item.dataSource
        self.player.play(url, item._listItem)


    def getCachedData(self):

        action = 'mcData'
        apiEndpoint = self.vader.apiEndpoint
        embedded = self.vader.embedded


        try:
            timeNow = time.time()
            url = 'http://{apiEndpoint}/getMatchCenter'.format(apiEndpoint=apiEndpoint)
            if embedded != True:
                utils.log('attempting to fetch ' + url)
            cacheFile = action
            cachePath = os.path.join(ADDONDATA, cacheFile)
            utils.log(cachePath)
            if os.path.exists(cachePath):
                fileTime = os.path.getmtime(cachePath)
                if timeNow - fileTime > 1200:
                    utils.log('deleting cache for fetch')
                    utils.delete(cachePath)

                    readString = requests.get(url).text
                    with open(cachePath, 'w') as cacheFp:
                        cacheFp.write(readString)

                else:
                    utils.log('using cache...')
                    with open(cachePath, 'r') as cacheFp:
                        readString = cacheFp.read()
                        try:
                            jsonTest = json.loads(readString)
                        except:
                            readString = requests.get(url).text
                            with open(cachePath, 'w') as cacheFp:
                                cacheFp.write(readString)


            else:
                readString = requests.get(url).text
                with open(cachePath, 'w') as cacheFp:
                    cacheFp.write(readString)

            return readString


        except Exception as e:
            if embedded != True:
                utils.log("Error fetching url \n{0}\n{1}".format(e, traceback.format_exc()))
            pass


    def mcList(self, category='all'):
        items = []



        category = plugintools.get_setting('mcLastCategory')
        if category == '' or category == None:
            category = 'all'

        plugintools.log('get mc category:' + category)
        self.programsList.reset()

        apiEndpoint = self.vader.apiEndpoint
        manualOffsetEnabled = plugintools.get_setting("mc_timezone_enable")
        mcBackward = float(plugintools.get_setting("mc_backward"))*60*60*-1
        mcForward = float(plugintools.get_setting("mc_forward"))*60*60

        username = self.vader.username
        password = self.vader.password
        embedded = self.vader.embedded





        if self.mcData == None:
            data = self.getCachedData()
            self.mcData = json.loads(data.decode('utf-8'))


        if manualOffsetEnabled == 'true' :
            offset = float(plugintools.get_setting('mc_timezone'))
            offset = offset * 60 * 60

        else:
            offset = 0


        timeNow = int(time.time())



        validItems = []
        itemsAdded = 0

        for epgItem in self.mcData:
            name = epgItem['name'].encode('utf-8')
            startTime = epgItem['startTime']
            endTime = epgItem['endTime']
            stream = epgItem['stream']


            addItem = False

            if int(endTime) > timeNow and int(startTime) < timeNow  :
                addItem = True


            if int(startTime) - timeNow < 0 and int(startTime) - timeNow > mcBackward:
                addItem = True

            if int(startTime) - timeNow > 0 and int(startTime) - timeNow < mcForward:
                addItem = True

            if addItem == True:
                validItems.append(epgItem)


        sortedEpg = sorted(validItems, key=lambda k: k['startTime'])

        for epgItem in sortedEpg:
            startTime = int(epgItem['startTime']) + int(offset)
            endTime = int(epgItem['endTime']) + int((offset))
            quality = epgItem['quality']
            ss_chan = epgItem['ss_stream']
            itemCategory = epgItem['category']
            name = epgItem['name']
            parentId = epgItem['parentId']

            if category.lower() in itemCategory.lower() or category.lower() in 'all':
                if '0' == parentId:
                    startTimeString = datetime.fromtimestamp(int(startTime)).strftime("%a - %H:%M")

                    title = '[COLOR crimson]' + itemCategory + '[/COLOR] ' + epgItem['name']
                    if embedded == True:
                        timeNow = time.time()
                        diffTime = timeNow % 3600
                        tokenTime = timeNow - diffTime
                        base = 'live'
                        extension = 'ts'
                        tokenString = username + password + str(epgItem['stream']) + str(tokenTime)
                        token = hashlib.md5(tokenString).hexdigest()
                        chanUrl = 'http://{apiEndpoint}/boxRedir?token={token}&stream={stream}&base={base}&extension={extension}&plugin={plugin}'.format(apiEndpoint=apiEndpoint, token=token, stream=epgItem['stream'],  base=base,extension=extension, plugin=ADDONID)
                    else:
                        chanUrl = 'http://%s/live/%s/%s/%s.%s' % (apiEndpoint,username, password, epgItem['stream'], 'ts')
                    listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
                    info_labels = {"Title": title, "FileName": title, "Plot": title}
                    listitem.setInfo("video", info_labels)
                    listitem.setProperty('IsPlayable', 'true')

                    item = kodigui.ManagedListItem(title, startTimeString, iconImage=None, data_source=chanUrl,
                                                   versions=epgItem['versions'])


                    qtex = ''
                    if endTime < time.time():
                        item.setProperty('old','old')

                    elif startTime <= time.time():
                        prog = ((timeNow - startTime) / float(endTime-startTime)) * 100

                        prog = int(prog - (prog % 5))
                        tex = 'progress/script-progress_{0}.png'.format(prog)
                        item.setProperty('playing', tex)

                    if epgItem['versions'] == None:
                        item.setProperty('channel', str('#'+ss_chan))
                        if '720p' in quality.lower():
                            qtex = 'script-hd_720p.png'
                        elif '1080i' in quality.lower():
                            qtex = 'script-hd_1080i.png'
                        elif 'UHD' in quality.lower():
                            qtex = 'script-hd_720p.png'

                    else:
                        for version in epgItem['versions']:
                            if '(720p' in version['name'].lower():
                                qtex = 'script-hd_720p.png'
                            elif '(1080i' in version['name'].lower():
                                qtex = 'script-hd_1080i.png'
                            elif '(UHD' in version['name'].lower():
                                qtex = 'script-hd_720p.png'

                    itemsAdded = itemsAdded + 1
                    items.append(item)
                    item.setProperty('quality',qtex)

        self.programsList.addItems(items)


        for i in range(len(items)):
            if not items[i].getProperty('old'):
                self.programsList.selectItem(i)
                break


        plugintools.log(str(itemsAdded))
        if itemsAdded == 0:
            plugintools.log('no events for category')
            item = kodigui.ManagedListItem('No Upcoming Events in {category}'.format(category=category), '', iconImage=None, data_source=None,
                                           versions=None)
            self.programsList.addItem(item)

        return True

class matchcenter():
    def __init__(self, ):
        self.window = None
        self.closedTime = 0

    def run(self):
        self.window = MyAddon('script-category.xml', utils.__addon__.getAddonInfo('path'), 'Main', '720p',
                         manager=None)


        self.window.doModal()

        # self.window.onClosed()
        plugintools.set_setting('mcClosedTime' , str(int(time.time())))
        del self.window
        self.window = None
