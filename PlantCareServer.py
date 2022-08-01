from flask import Flask, redirect, url_for, request
from flask import jsonify
from flask import make_response
import ChangeWordpressPost
import datetime
import pytz
import hashlib

passwd = "HELLO"
def compareToken(passwd,usr_token):
    nowtime = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    nowtimeStr = nowtime.strftime('%Y-%m-%d %H:%M')
    pre_token = nowtimeStr+passwd
    token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
    print(pre_token,token,usr_token)
    if(token == usr_token):
        return True
    else:
        return False

app = Flask(__name__)

JSON_RESPONSE_CONTENT_TYPE = 'application/json;charset=UTF-8'
def _custom_response(json_string):
    response = make_response(jsonify(json_string))
    response.headers['Content-Type'] = JSON_RESPONSE_CONTENT_TYPE
    return response


@app.route('/plantcare/',methods = ['POST'])
def plantcare_post():
   if request.method == 'POST':
        text_content = ""

        flowerName = ChangeWordpressPost.getFlower(request.json["flower"])
        actionName = ChangeWordpressPost.getAction(request.json["action"])

        #print(request.json["flower"],flowerName)
        #print(request.json["action"],actionName)

        #身份验证
        usr_token = request.json["token"]
        if(not compareToken(passwd,usr_token)):
            return _custom_response("🔒🔒🚫🚫权限错误!")

        if(flowerName != None and actionName != None):
            client = ChangeWordpressPost.getclient()
            #获取文章
            post = ChangeWordpressPost.getWordpressPost(client,request.json["flower"])

            #更新文档动作日期
            post = ChangeWordpressPost.updatePlant(actionName,post)
            if(request.json["action"] == "1"): #如果是浇水则更新标题
                post = ChangeWordpressPost.updatePlantTitle(post)

            #更新文档并且输出log
            if(ChangeWordpressPost.EditPost(client,request.json["flower"],post)):
                text_content = "🪴🪴🥰🥰"+flowerName+actionName+"完成!"
                #print(flowerName+" "+ actionName+"更新完成！")
            else:
                text_content = "🪴🪴😱😱"+flowerName+actionName+"失败!"
                #print(flowerName+" "+ actionName+"更新失败！")
        else:
                text_content = "🤕🤕🤕🤕指令错误!"
                #print("指令错误！")

        return _custom_response(text_content)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000)