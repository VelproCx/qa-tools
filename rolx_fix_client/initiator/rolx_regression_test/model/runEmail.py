#!/usr/bin/env python
# -*- coding:utf-8 -*-
# fileName: run_email.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr


# 定义发邮件
def send_mail(file_path):
    assert isinstance(file_path, list)

    smtpserver = 'email-smtp.ap-northeast-1.amazonaws.com'
    port = 465  # Amazon SES SMTP端口为465
    user = 'AKIATDLW3JI55OXL6PJE'
    password = 'BKusrtLwYnincf9wWNeXw008BfHrhLbMAoSkPUwzcAkD'

    sender = 'no-reply@finstadiumx.co.jp'
    # 可添加多个收件人的邮箱
    receives = ['huangmiaolan@farsightedyu.com', 'zhangtaotao@farsightedyu.com',
                'zhenghuaimao@farsightedyu.com', 'xiang.chen@farsightedyu.com']

    # 构造邮件对象
    msg = MIMEMultipart('mixed')
    # 定义邮件的标题
    subject = '【ROLX】【SIT】Rol Regression Test Report'
    # HTML邮件正文，定义成字典
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = formataddr(('FSX', sender))
    msg['To'] = ','.join(receives)
    # 构造文字内容
    text_plain = MIMEText("Regression Result，Please check the attachment.", 'html', 'utf-8')
    msg.attach(text_plain)
    # 构造附件

    for file in file_path:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{file}"')
        msg.attach(part)

    context = smtplib.SMTP_SSL(smtpserver, port)
    context.login(user, password)

    print("开始发送邮件...")
    context.sendmail(sender, receives, msg.as_string())
    print("已发送邮件")
    return
