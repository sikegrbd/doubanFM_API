#coding=utf-8
#This is a modle of DoubanFM
import json
import requests
import contextlib
import time
import os

def loginFM(usernameOfFM,passwordOfFM): #添加错误处理代码
   #通过POST传输登录信息登录
   loginData={"apikey":"02646d3fb69a52ff072d47bf23cef8fd","client_id":"02646d3fb69a52ff072d47bf23cef8fd","client_secret":"cde5d61429abcd7c","udid":"b88146214e19b8a8244c9bc0e2789da68955234d","douban_udid":"b635779c65b816b13b330b68921c0f8edc049590","device_id":"b88146214e19b8a8244c9bc0e2789da68955234d","grant_type":"password","redirect_uri":"http://www.douban.com/mobile/fm","username":usernameOfFM,"password":passwordOfFM}
   headerDict={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/x-www-form-urlencoded"}
   doubanFmUrl="https://www.douban.com/service/auth2/token"
   reciveOfFM=requests.post(doubanFmUrl,data=loginData,headers=headerDict)
   return json.loads(reciveOfFM.text)

def getChanelList():
   #通过GET获取频道列表
   #"client":"s:mobile|y:iOS 10.2|f:115|d:b88146214e19b8a8244c9bc0e2789da68955234d|e:iPhone7,1|m:appstore"
   getData={"alt":"json","app_name":"radio_iphone","apikey":"02646d3fb69a52ff072d47bf23cef8fd","client":"s:mobile","client_id":"02646d3fb69a52ff072d47bf23cef8fd","icon_cate":"xlarge","udid":"b88146214e19b8a8244c9bc0e2789da68955234d","douban_udid":"b635779c65b816b13b330b68921c0f8edc049590","version":"115"}
   getUrl="https://api.douban.com/v2/fm/app_channels"
   headerDict={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
   reciveOfFM=requests.get(getUrl,params=getData,headers=headerDict)
   return json.loads(reciveOfFM.text)

def getNowSing(channel_id,user_name="",access_token="",isLogin=0):
   #通过GET获取歌曲列表
   #获取歌曲列表,参数为0表示未登录,否则表示登录
   #Header的Authorization字段未登录不填,填则表示登录
   #"client":"s:mobile|y:iOS 10.2|f:115|d:b88146214e19b8a8244c9bc0e2789da68955234d|e:iPhone7,1|m:appstore"
   getData={"channel":channel_id,"from":"mainsite","type":"n","pt":"0.0","kbps":"128","formats":"aac","alt":"json","app_name":"radio_iphone","apikey":"02646d3fb69a52ff072d47bf23cef8fd","client":"s:mobile|y:iOS 10.2|f:115|d:b88146214e19b8a8244c9bc0e2789da68955234d|e:iPhone7,1|m:appstore","icon_cate":"xlarge","udid":"b88146214e19b8a8244c9bc0e2789da68955234d","douban_udid":"b635779c65b816b13b330b68921c0f8edc049590","version":"115"}
   getUrl="https://api.douban.com/v2/fm/playlist"
   headerDict={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
   if isLogin==1:
      headerDict["Authorization"]=user_name+" "+access_token
   reciveOfFM=requests.get(getUrl,params=getData,headers=headerDict)
   return json.loads(reciveOfFM.text)

def upSentFeel(action,user_id="",access_token="",expire=0,isLogin=0):
   #通过GET歌曲操作上报
   # tlDust='b'
   # tsEnd='e'
   # tlNew='n'
   # tlPlaying='p'
   # tsSkip='s'
   # tsLike='r'
   # tsCancelLike='u'
   if isLogin==1:
      report["user_id"]=user_id
      report["token"]=access_token
      report["expire"]=expire
   reportUrl="https://api.douban.com/v2/fm/playlist"
   report={"app_name":"radio_android","version":100,"type":action}
   headerDict={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
   reciveOfFM=requests.get(reportUrl,params=report,headers=headerDict)
   return json.loads(reciveOfFM.text)

def getLyric(songSid,songSsid):
   #通过GET获取歌词
   getUrl="https://api.douban.com/v2/fm/lyric"
   getReport={"sid":songSid,"ssid":songSsid};
   headerDict={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
   reciveOfFM=requests.get(getUrl,params=getReport,headers=headerDict)
   return json.loads(reciveOfFM.text)

rmSwitch=0; #1代表删除临时的音频文件,0代表保留临时的音频文件
loginDict=loginFM("sikegrbd@163.com","a154828813")
channelDict=getChanelList()
for i in range(len(channelDict["groups"])):
   print("group_id: "+str(channelDict["groups"][i]["group_id"]))
   for t in range(len(channelDict["groups"][i]["chls"])):
      print("channel: "+channelDict["groups"][i]["chls"][t]["name"]+"\nchannel_id: "+str(channelDict["groups"][i]["chls"][t]["id"]))
while True:
   nowSingDict=getNowSing(7,"sike",loginDict["access_token"],0)
   # print(nowSingDict)
   print("title: "+nowSingDict["song"][0]["title"]+"=>singer: "+nowSingDict["song"][0]["singers"][0]["name"]+"\nsid: "+nowSingDict["song"][0]["sid"])
   songName=nowSingDict["song"][0]["title"]
   songSsid=nowSingDict["song"][0]["ssid"]
   songSid=nowSingDict["song"][0]["sid"]
   fileFormat=nowSingDict["song"][0]["file_ext"]
   songUrl=nowSingDict["song"][0]["url"]
   fileSha256=nowSingDict["song"][0]["sha256"]
   with contextlib.closing(requests.get(songUrl,stream=True)) as response:
      chunk_size=1024 #单次最大请求
      content_size=int(response.headers['content-length']) #内容总体积大小
      with open("./songs/"+songName,"wb") as file:
         for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
   os.system("vlc --play-and-exit \"./songs/"+songName+"\"")
   if rmSwitch==1:
      os.system("rm \"./songs/"+songName+"\"")
   #send "I like this song"
   upSentFeel("r",user_id=loginDict["douban_user_id"],access_token=loginDict["access_token"],expire=loginDict["expires_in"],isLogin=1)