# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts,media
import re
import datetime
import pytz
import ServerInfo

plantDic = {
            "44":"无尽夏（大）", 
            "58":"无尽夏（小）", 
            "62":"紫叶酢浆草", 
            "64":"乒乓菊", 
            "66":"无尽夏扦插苗", 
            "68":"香雪兰种子1", 
            "70":"香雪兰种子2", 
        }

actionDic = {
            "1":"浇水", 
            "2":"施肥", 
            "3":"打药", 
        }

#检查花的id是否存在并且获取花名
def getFlower(id):
        try:
                return plantDic[id]
        except:
                return

#检查动作id是否合法并且获取动作
def getAction(id):
        try:
                return actionDic[id]
        except:
                return


#更新内容函数
def updatePlant(value,_post):
        nowtime = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        nowtimeStr = nowtime.strftime('%Y-%m-%d')

        pattern = f'<li>{value}：(.*?)</li>'
        lastdaycontent = f"今天刚{value[0]}过{value[1]}"
        repl = f'<li>{value}：{nowtimeStr} ({lastdaycontent})</li>'
        _post.content = re.sub(pattern, repl, _post.content, count=0, flags=0)
        return _post

#比较时间
def compare_time(time1,time2):
        d1 = datetime.datetime.strptime(time1, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(time2, '%Y-%m-%d')
        delta = d1 - d2
        return delta.days

#更新所有内容函数
def updatePlantAllContent(_post):
        nowtime = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        nowtimeStr = nowtime.strftime('%Y-%m-%d')

        #获取标题
        title = _post.title
        pattern = '(.*)：(.*)'
        title0 = re.search(pattern,title).group(1) 
        #获取上次浇水时间
        water_pattern = '<li>浇水：(.*?)</li>'
        last_water_day = re.search(water_pattern,_post.content).group(1).split(" ")[0]
        day = compare_time(nowtimeStr,last_water_day)
        if(day!=0):
                title1 = day.__str__()+"天前浇过水"
        else:
                title1 = "今天刚浇过水"
        repl = f'{title0}：{title1}'
        _post.title = re.sub(pattern, repl, _post.title, count=0, flags=0)

        updateContentLastDay(_post,actionDic["1"],nowtimeStr)
        updateContentLastDay(_post,actionDic["2"],nowtimeStr)
        updateContentLastDay(_post,actionDic["3"],nowtimeStr)
        
        return _post

def updateContentLastDay(_post,action_value,nowtimeStr):
        pattern = f'<li>{action_value}：(.*?)</li>'
        lastday = re.search(pattern,_post.content).group(1).split(" ")[0]
        day = compare_time(nowtimeStr,lastday)

        if(day!=0):
                lastdaycontent = day.__str__()+f"天前{action_value[0]}过{action_value[1]}"
        else:
                lastdaycontent = f"今天刚{action_value[0]}过{action_value[1]}"

        repl = f'<li>{action_value}：{lastday} ({lastdaycontent})</li>'
        _post.content = re.sub(pattern, repl, _post.content, count=0, flags=0)
        return _post


#根据id获取文章
def getWordpressPost(client,plantName):
        post = client.call(posts.GetPost(plantName))
        return post

#post = updatePlant("浇水",post)
#post = updatePlantTitle(post)

def getclient():
        return Client(ServerInfo.address+"/xmlrpc.php",ServerInfo.usr,ServerInfo.password)

def EditPost(client,plantName,_post):
        return client.call(posts.EditPost(plantName,_post))