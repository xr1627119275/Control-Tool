# -*- coding: UTF-8 -*-
import tornado.ioloop
import tornado.websocket
from tornado.httpserver import HTTPServer
import tornado.web
import datetime
import re,json,os

import configparser
conf = configparser.ConfigParser()
conf_path = os.path.dirname(os.path.realpath(__file__)) + "/config.ini"
conf.read(conf_path)

'''
发送服务器命令
{
  content: 'mibook<<exec:dir', // 'ls' 'mibook'
  from: 'Server' 
}
'''
class StaticFile(tornado.web.StaticFileHandler):  
    def set_extra_headers(self, path):  
        self.set_header("Cache-control", "no-cache")  

class ServerHandler(tornado.web.RequestHandler):
    uploadFilePath = os.path.join(conf.get('Server','uploadPath'),'')
    def get(self):
        self.write("请使用POST上传")
    def post(self):
        file_metas = self.request.files.get('file')
        if file_metas == None:
          self.write("上传失败")
          return
        for meta in file_metas:                                 #循环文件信息
          file_name = meta['filename']                        #获取文件的名称                                         #引入os路径处理模块
          if not os.path.exists(self.uploadFilePath):
            os.mkdir(self.uploadFilePath)
          with open(os.path.join(self.uploadFilePath,file_name),'wb') as up:            #os拼接文件保存路径，以字节码模式打开
              up.write(meta['body'])
        self.write("上传成功")

users = set()
class WebSocketHandler(tornado.websocket.WebSocketHandler):
  target = 'None'
  def check_origin(self, origin):  
      return True  
  def open(self, *args, **kwargs):
      '''客户端连接'''
      print("connect....")
      print(self.request)
      users.add(self)

  def ServerCommand(self,message,user_from):
      # print(message)
      if message.startswith('login:'):
        user = message[6:].strip()
        for client in users:
          if client == self or client.target == user:
            client.target = user
            client.write_message(json.dumps({'content':'登录成功','from':'Server'}).encode('utf8'))
            return -1
        return 0

      if message == 'ls':
        content = '序号\t用户名\n'
        index = 0
        for client in users:
          content +=  str(index)+'\t'+client.target+'\n'
          index+=1
        self.write_message(json.dumps({'content':content,'from':'Server'}).encode('utf8'))    
        return 0


      if message.find('<<') != -1 :
        content = re.findall(r'(\S+?)<<(.+)',message,re.S)
        if len(content) != 1 or len(content[0]) !=2:
          return -1
        content = content[0]

        for client in users:
          if client.target == content[0]:
            client.write_message(json.dumps({'content':content[1],'from':user_from}).encode('utf8'))
        # self.write_message(content.encode('utf8'))
        return 0

      return -1
  def on_message(self, message):
      '''有消息到达'''
      message = json.loads(message)
      code = self.ServerCommand(message['content'],message['from'])
      if code != 0:
        # print(message)
        self.write_message(message)

      # now = datetime.datetime.now()
      # content = self.render_string("recv_msg.html",date=now.strftime("%Y-%m-%d %H:%M:%S"),msg=message)
      # content = message.encode('utf8')
      # for client in users:
      #   if client == self:
      #       continue
      # self.write_message(message)

  def on_close(self):
      '''客户端主动关闭连接'''
      users.remove(self)

settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
  ("/",WebSocketHandler),
  ("/Upload",ServerHandler)
],**settings)


if __name__ == "__main__":
    # server = HTTPServer(application,ssl_options={
    #   "certfile": os.path.join(os.path.abspath("."), "*.crt"),
    #   "keyfile": os.path.join(os.path.abspath("."), "*.key"),
    # })
    application.listen(7998,address='0.0.0.0')
    # server.listen(7999,address='0.0.0.0')

    #io多路复用
    tornado.ioloop.IOLoop.instance().start()