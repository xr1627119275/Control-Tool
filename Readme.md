


## 浏览器 控制端
  # js 代码
  ```js
    function Lianjie(name,ip){
      var ws = new WebSocket(ip);
    
      ws.onopen = function()
      {
        // Web Socket 已连接上，使用 send() 方法发送数据
        ws.send(`${JSON.stringify({"content":"login:"+name,from:name})}`);
        console.log("数据发送中...");
      };

      ws.onmessage = function (evt) 
      { 
        var received_msg = evt.data;
        console.log("From:"+JSON.parse(received_msg)['from']);
        console.log(JSON.parse(received_msg)['content']);
      }
      ws.onclose = function()
      { 
        // 关闭 websocket
        console.log("连接已关闭..."); 
        console.log("2秒后重连..."); 
      
        setTimeout(function(){
          ws = new WebSocket(ip);
        },2000)
      };
      this.send = function(content){
        ws.send(JSON.stringify({content:content,from:name}))
      }
      this.exec = function(who,content){
        ws.send(JSON.stringify({content:who+"<<exec:"+content,from:name}))
      }
      this.im = this.IM = function(who,content){
        ws.send(JSON.stringify({content:who+"<<IM:"+content,from:name}))
      }
      this.work = function(who,content){
        ws.send(JSON.stringify({content:who+"<<work:"+content,from:name}))
      }
  }
  ```