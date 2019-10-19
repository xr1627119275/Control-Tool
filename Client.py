# -*- coding: UTF-8 -*-

import websocket
import os,json,time,sys
import requests
import _thread
import configparser
from Email import SendEmail


conf = configparser.ConfigParser()
conf_path = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
conf.read(conf_path)

login = conf.get("Client", "login")
if len(sys.argv) >= 2:
    login = sys.argv[1]
    

closeConnent = 0
errors = 0


def upload(path):
    return os.stat(path)

def sendMsg(ws,msg,_form):
    msg = json.dumps({
        'content':_form+'<<result:\n'+msg,
        'from': login
    })
    ws.send(msg.encode('utf8'))

def on_message(ws, message):
    message = json.loads(message)
    global closeConnent

    closeConnent = 0
    print("\nFrom: "+message['from'])

    if message['content'].startswith('im:') or message['content'].startswith('IM:'):
        print("From: "+message['from']+'\n'+message['content'][3:])
        return
    if message['content'].startswith('result:'):
        print(message['content'][7:])
        return
    if message['content'].startswith('work:'):
        os.chdir(message['content'][5:])
        os.path.realpath
        print(os.getcwd())
        return 
    if message['content'].startswith('upload:'):
        path = message['content'][7:]
        if os.path.isfile(path):
            files = {'file': (os.path.basename(path), open(os.path.realpath(path), 'rb'))}
            try:
                result = requests.post(conf.get("Client", "UploadUrl"),files=files)
                print(result.content)
                if result.status_code==200:
                    sendMsg(ws,result.content.decode('utf8'),message['from'])
                else:
                    sendMsg(ws,'上传失败 %d'%result.status_code,message['from'])
            except Exception as e:
                sendMsg(ws,'上传失败, %s'%str(e),message['from'])  

        else:
            sendMsg(ws,'不支持文件夹 or 无此文件',message['from'])
        return 
    elif message['content'].startswith('exec:'):
        execMsg = ''
       
        with os.popen(message['content'][5:]) as f:
            execMsg += f.read()
        sendMsg(ws,execMsg,message['from'])
        # print(message['content'][5:])
        # print(execMsg)
        
        return
    print(message['content'])
    

def on_error(ws, error):
    global closeConnent
    closeConnent += 1
    if closeConnent == 10:
        SendEmail(login,'服务器离线')

    print('服务器重连中...')
    time.sleep(10)
    main()

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    #global login
    #login = input('Login:')
    #loginContent = 'login:'+login
    print('open')
    ws.send(json.dumps({'content':'login:'+login,'from':login}).encode('utf8'))
    # while True:
    #     msg = input('输入:')
    #     ws.send(json.dumps({'content':msg,'from':login}).encode('utf8'))

def main():
    # global errortime
    # if errortime == 10 :
    #     os.popen('shutdown -s -t 120')
    #     print('2分钟后关机')
    #     return
    # errortime +=1
    ws = websocket.WebSocketApp(conf.get("Client", "Ws"),
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    
    ws.run_forever()


def testInternet():
    global errors

    while True:
        time.sleep(10)
        try:
            if errors == 4:
                os.popen('shutdown -s -t 300')
                print('5分钟后关机')
                return
            res = requests.get('http://www.baidu.com',timeout=10)
            # print(res.status_code)
            if res.status_code == 200:
                errors = 0
        except Exception as e:
            if isinstance(e, requests.exceptions.Timeout):
                errors += 1
                print('error time: %d'%errors)



if __name__ == "__main__":

    websocket.enableTrace(True)
    _thread.start_new_thread(testInternet,())
    main()
    
