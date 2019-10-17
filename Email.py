import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def SendEmail(_from,content):
  user_name = _from
  receiver = "1627119275@qq.com"  # 接收邮件账户
  sender = "15956965998@163.com"  # 发送邮件账户
  pwd = "XRxr13275708870"  # smtp密钥 具体可以到QQ邮箱获取
  msg = MIMEMultipart()
  msg["Subject"] = "%s的实时信息！" % user_name  # 邮件的主题
  msg["From"] = sender
  msg["To"] = receiver

  part = MIMEText("%s的信息\n %s" % (user_name,content))  # 邮件的正文
  msg.attach(part)

  # jpg类型附件
  # onImage()
  # part = MIMEApplication(open('_screenshot.bmp', 'rb').read())  #  'screenshot.bmp'和该.py文件在同一个文件夹下
  # part.add_header('Content-Disposition', 'attachment', filename="screenshot.jpg")
  # msg.attach(part)

  try:
      s = smtplib.SMTP("smtp.163.com", timeout=30)  # 连接smtp邮件服务器,端口默认是25
      s.ehlo()
      s.starttls()
      s.login(sender, pwd)  # 登陆服务器
      s.sendmail(sender, receiver, msg.as_string())  # 发送邮件
      s.close()
      print('邮件发送成功！')
  except smtplib.SMTPException:
      print('邮件发送失败！')


if __name__ == "__main__":
    SendEmail('xurui','测试')