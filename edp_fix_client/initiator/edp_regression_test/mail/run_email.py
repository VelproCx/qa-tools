#!/usr/bin/env python
# -*- coding:utf-8 -*-
# fileName: run_email.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

from email.mime.base import MIMEBase
from email import encoders


# 定义发邮件
def send_mail(file_path=[]):
    assert isinstance(file_path, list)

    smtpserver = 'smtp.exmail.qq.com'
    # 设置登录邮箱的账号和授权密码
    user = 'xiang.chen@farsightedyu.com'
    password = "qffbzdwNgCVBF83y"
    sender = 'xiang.chen@farsightedyu.com'
    # 可添加多个收件人的邮箱
    receives = ['sophie.yang@finstadiumx.co.jp', 'osamu.tachibana@finstadiumx.co.jp',
                'zhangtaotao@farsightedyu.com', 'zhenghuaimao@farsightedyu.com', 'xiang.chen@farsightedyu.com']

    # receives = [
    #     'zhangtaotao@farsightedyu.com', 'zhenghuaimao@farsightedyu.com', 'xiang.chen@farsightedyu.com']

    # 构造邮件对象
    msg = MIMEMultipart('mixed')
    # 定义邮件的标题
    subject = '【SIT】edp_regression_test report'
    # HTML邮件正文，定义成字典
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = sender
    msg['To'] = ','.join(receives)
    # 构造文字内容
    text_plain = MIMEText("Regression Result，Please check the attachment.", 'html', 'utf-8')
    msg.attach(text_plain)
    # 构造附件

    for file in file_path:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file.split("/")[-1])
        msg.attach(part)

    # 邮箱设置时勾选了SSL加密连接，进行防垃圾邮件，SSL协议端口号要使用465
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    # 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 向服务器返回确认结果
    smtp.ehlo(smtpserver)
    # 登录邮箱的账号和授权密码
    smtp.login(user, password)

    print("开始发送邮件...")
    # 开始进行邮件的发送，msg表示已定义的字典
    smtp.sendmail(sender, receives, msg.as_string())
    smtp.quit()
    print("已发送邮件")
    return
send_mail(['../report/edp_report.xlsx', '../logs/edp_report.log'])