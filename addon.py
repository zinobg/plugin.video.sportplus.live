# -*- coding: utf-8 -*-
from urllib2 import Request,urlopen
from re import compile as Compile
from xbmc import log,translatePath
from xbmcgui import Dialog
from xbmcswift2 import Plugin
from json import loads as Loads

BASE='https://en.sportplus.live'

plugin=Plugin()

live_icon=translatePath(plugin.addon.getAddonInfo('path')+'/resources/live.png')
clock_icon=translatePath(plugin.addon.getAddonInfo('path')+'/resources/clock.png')

@plugin.route('/')
def menu_index():
    try: 
        '''
        it is supported only in newer versions of kodi
        '''
        menu=Dialog().contextmenu(['Football','Tennis','Basketball','Ice Hockey','Baseball','Rugby','Table Tennis','Valleyball','Austranlian Rules'])
    except:
        menu=Dialog().select('',['Football','Tennis','Basketball','Ice Hockey','Baseball','Rugby','Table Tennis','Valleyball','Austranlian Rules'])
    if menu==0:
        plugin.redirect(plugin.url_for('open_live',sport='football'))
    if menu==1:
        plugin.redirect(plugin.url_for('open_live',sport='tennis'))
    if menu==2:
        plugin.redirect(plugin.url_for('open_live',sport='basketball'))
    if menu==3:
        plugin.redirect(plugin.url_for('open_live',sport='ice_hockey'))
    if menu==4:
        plugin.redirect(plugin.url_for('open_live',sport='baseball'))
    if menu==5:
        plugin.redirect(plugin.url_for('open_live',sport='rugby'))
    if menu==6:
        plugin.redirect(plugin.url_for('open_live',sport='table_tennis'))
    if menu==7:
        plugin.redirect(plugin.url_for('open_live',sport='volleyball'))
    if menu==8:
        plugin.redirect(plugin.url_for('open_live',sport='australian_rules'))

@plugin.route('/live/<sport>')
def open_live(sport):
    log('path: [/live/'+sport+']')
    source=openUrl(BASE+'/'+sport)
    match=Compile('<a class="preview__link" href="(.+?)">.*\n.(.+?)<\/div>\n.*\n.*class="preview__vs-live".*\n.*\n.*class="preview__team preview__team--left">\n(.+?)<\/div>').findall(source)
    items=[{'label':home.strip()+' - '+guest.strip(),'icon':live_icon,'thumbnail':live_icon,'path':plugin.url_for('play_live',url=BASE+url)} for url,home,guest in match]
    if len(items) == 0:
        items.append({'label':'NO LIVE ['+sport+'] ACTIVITY!','icon':live_icon,'thumbnail':live_icon,'path':plugin.url_for('open_live',sport=sport)})
    match=Compile('(<div class="preview__date preview__date--white">(.+?)<\/div>.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)*(<div class="preview__team preview__team--right">\n.(.+?)<\/div>\n.*\n.*<div class="preview__time">(.+?)<\/div>\n.*\n.*\n.(.+?)<\/div>)').findall(source)
    for temp1,day,temp2,team1,time,team2 in match:
        if day:
            items.append({'label':'['+day+']','path':plugin.url_for('open_live',sport=sport)})
        items.append({'label':'['+time+' UTC+3] '+team1.strip()+' - '+team2.strip(),'icon':clock_icon,'thumbnail':clock_icon,'path':plugin.url_for('open_live',sport=sport)})
    return plugin.finish(items)

@plugin.route('/stream/<url>')
def play_live(url):
    log('path: [/stream/'+url+']')
    source=openUrl(url)
    match=Compile('<div data-player="(.+?)"><\/div>').findall(source)
    json_list=match[0].replace("&quot;", "\"");
    json_list=Loads(json_list)
    item={'label':'','path':json_list["channels"][0]["sources"][1]}
    plugin.play_video(item)
    return plugin.finish(None,succeeded=False)
    
def openUrl(url):
    req=Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
    response=urlopen(req)
    source=response.read()
    response.close()
    return source

def main():
    plugin.run()

if __name__ == '__main__':
    main()