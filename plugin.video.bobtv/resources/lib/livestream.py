import xbmcaddon
import urllib, urllib2, re, os, json, xbmc, xbmcgui, xbmcaddon, xbmcplugin, time, sys 
from StringIO import StringIO
from datetime import timedelta
from bigoldboy import *   # biggy's functions

IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4'
LIVESTREAM_UA = 'Livestream/3.8.12/Nemiroff (iPhone; iOS 8.4; Scale/2.00)'
selfAddon = xbmcaddon.Addon(id='plugin.video.bobtv') # points to our addon

def get_livestream(owner_id,event_id,video_id):    

    m3u8_url = ''
    tl(str(owner_id))
    tl(str(event_id))
    tl(str(video_id))
    if video_id == None:  # comes here the first time
        url = 'https://api.new.livestream.com/accounts/'+owner_id+'/events/'+event_id+'/'                
        req = urllib2.Request(url)       
        req.add_header('User-Agent', IPHONE_UA)
        response = urllib2.urlopen(req)                    
        json_source = json.load(response)
        response.close()
        
        if json_source['stream_info'] is not None:            
            event_info = EXTRACT_EVENT_INFO(json_source['stream_info']['live_video_post'])
            icon = ''
            try:
                icon = json_source['stream_info']['thumbnail_url']
            except:
                pass
        
        feed_total = str(json_source['feed']['total'])
        url = 'https://api.new.livestream.com/accounts/'+owner_id+'/events/'+event_id+'/feed/?maxItems='+feed_total
        req = urllib2.Request(url)       
        req.add_header('User-Agent', IPHONE_UA)
        response = urllib2.urlopen(req)                    
        json_source = json.load(response)
        response.close()
        
        for event in json_source['data']:                         
            try:
                event_info = EXTRACT_EVENT_INFO(event['data'])                    
                addStream(event_info['name'],'/live_now',event_info['name'],event_info['icon'],event_info['fanart'],event_id,owner_id,event_info['info'],event_info['broadcast_id'])
            except:
                pass          
        return get_livestream(owner_id,event_id,'LIVE')  
    else:     
        if video_id == 'LIVE':
            url = 'https://api.new.livestream.com/accounts/'+owner_id+'/events/'+event_id
            tl("url="+url)
            req = urllib2.Request(url)
            req.add_header('User-Agent', IPHONE_UA)              
            response = urllib2.urlopen(req)      
            json_source = json.load(response)
            response.close()  
            ron=json_source['stream_info']['m3u8_url']
            return STREAM_QUALITY_SELECT(ron)
            
        else:
            url = 'https://api.new.livestream.com/accounts/'+owner_id+'/events/'+event_id+'/videos/'+video_id            
            req = urllib2.Request(url)
            req.add_header('User-Agent', IPHONE_UA)              
            response = urllib2.urlopen(req)      
            json_source = json.load(response)
            response.close()
            STREAM_QUALITY_SELECT(json_source['m3u8_url'])

def GET_STREAM_QUALITY(m3u8_url):
    stream_url = []
    stream_title = [] 
    print "M3U8!!!" + m3u8_url
    req = urllib2.Request(m3u8_url)
    response = urllib2.urlopen(req)                    
    master = response.read()
    response.close()
    cookie = ''
    try:
        cookie =  urllib.quote(response.info().getheader('Set-Cookie'))
    except:
        pass

    print cookie
    print master        
    x=1
    y=1
    line = re.compile("(.+?)\n").findall(master)  
    for temp_url in line:
        if '.m3u8' in temp_url:
            x=x+1
            print temp_url
            print desc                  
            temp_url = temp_url+'|User-Agent='+IPHONE_UA              
            if cookie != '':
                temp_url = temp_url + '&Cookie='+cookie
            stream_url.append(temp_url)
            stream_title.append(str(desc))
        else:
            desc = ''
            y=y+1
            start = temp_url.find('RESOLUTION=')
            if start > 0:
                start = start + len('RESOLUTION=')
                end = temp_url.find(',',start)
                desc = temp_url[start:end]
                desc = desc + "0"
            else:
                desc = "Audio"

    return stream_url, stream_title

    
def STREAM_QUALITY_SELECT(m3u8_url):    
    
    stream_url, stream_title = GET_STREAM_QUALITY(m3u8_url)
    tl("stream_url="+str(stream_url))
    tl("stream_title="+str(stream_title))

    if len(stream_title) > 0:
        ret = 0
        AUTO_PLAY = selfAddon.getSetting('auto_best')        
        if AUTO_PLAY == 'true':            
            temp_qlty = 0
            i = 0
            for stream in stream_title:
                stream = stream.partition("x")[0]
                print stream
                print stream[1:]
                try:
                    if int(stream[1:]) > temp_qlty:
                        temp_qlty = int(stream[1:])
                        ret = i
                except:
                    pass
                i=i+1
        else:            
            dialog = xbmcgui.Dialog() 
            ret = dialog.select('Choose Stream Quality', stream_title)
        if ret >=0:
            return str(stream_url[ret])
        else:
            sys.exit()
    else:
        msg = "No playable streams found."
        dialog = xbmcgui.Dialog() 
        ok = dialog.ok('Streams Not Found', msg)

def EXTRACT_EVENT_INFO(event):
    
    event_info = {}             
    try:
        event_id = str(event['event_id'])
    except:
        event_id = str(event['id'])

    broadcast_id = None
    try:
        broadcast_id = str(event['id'])        
    except:
        broadcast_id = str(event['broadcast_id'])        

    try:
        name = event['full_name'].encode('utf-8')        
    except:
        name = event['caption'].encode('utf-8')

    icon = None
    fanart = None
    try:
        icon = event['logo']['url'].encode('utf-8')           
        fanart = event['background_image']['url'].encode('utf-8')        
    except:
        try:            
            icon = event['thumbnail_url'].encode('utf-8')  
        except:
            pass         

    try:
        start_time = str(event['start_time'])   
    except:
        try:
            start_time = str(event['streamed_at'])
        except:
            start_time = str(event['publish_at'])

    duration = 0
    try:
        duration = int(item['duration'])
    except:        
        pass

    desc = ''
    try:
        desc = str(event['description']).encode('utf-8')
    except:
        pass
    
    aired = start_time[0:4]+'-'+start_time[5:7]+'-'+start_time[8:10]
    info = {'plot': desc,'tvshowtitle':'Livestream','title':name,'originaltitle':name,'duration':duration,'aired':aired}
    event_info = {'name':name, 'event_id':event_id, 'icon':icon, 'fanart':fanart, 'info':info, 'broadcast_id':broadcast_id}

    return event_info


