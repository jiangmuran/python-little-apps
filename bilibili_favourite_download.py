import requests
import os
import time

def jx(jsontext):
    null=None
    true=True
    false=False
    return eval(jsontext)

#https://api.bilibili.com/x/v3/fav/resource/list?media_id=1817029963&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp


splist=[]

i=1
while True:
    text=jx(requests.get('https://api.bilibili.com/x/v3/fav/resource/list?media_id=1817029963&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp&pn='+str(i)).text)
    if(text['data']['medias'] != None):
        for j in text['data']['medias']:
            splist.append({'title':j['title'],'bv':j['bvid']})
    else:
        break
    i+=1
    print(i)

print(splist)
for i in splist:
    os.system('you-get -o ./output https://www.bilibili.com/video/'+i['bv'])
    print(str(len(splist))+'/'+str(splist.index(i)+1))
    time.sleep(3)

