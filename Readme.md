


# 浏览器 控制端
  ## js 代码
  ```js
    function Lianjie(name,ip){
    var ws = new WebSocket(ip);
	  var toUser = ''
	
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

    this.SetToUser = function(name) {
      toUser = name
    }
    this._send = function(content){
      //ws.send(JSON.stringify({content:content,from:name}))
      ws.send(JSON.stringify(content))
    }
    this.exec = function(content){
      //ws.send(JSON.stringify({content:who+"<<exec:"+content,from:name}))
          this._send({content:toUser+"<<exec:"+content,from:name})
    }
    this.im = this.IM = function(content){
      this._send({content:toUser+"<<IM:"+content,from:name})
    }
    this.work = function(content){
      this._send({content:toUser+"<<work:"+content,from:name})
    }
    this.upload = function(content){
      this._send({content:toUser+"<<upload:"+content,from:name})
    }
}
  ```