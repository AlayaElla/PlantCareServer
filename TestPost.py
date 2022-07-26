import requests
import os
import json
import datetime
import pytz
import hashlib

def calcToken(passwd):
    nowtime = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    nowtimeStr = nowtime.strftime('%Y-%m-%d %H:%M')
    pre_token = nowtimeStr+passwd
    print(pre_token)
    token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
    print(token)
    return token


passwd = "HELLO"
url = 'http://127.0.0.1:8000/plantcare'

my_token = calcToken(passwd)

post_json = {"flower":"44","action":"1","token":f"{my_token}"}

print(post_json)
r = requests.post(url, json=post_json, headers = {"Content-Type" : "application/json"})
print (r.status_code, r.text)
os.system("pause")