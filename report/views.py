from django.shortcuts import render

import os
import sys
# 현재 모듈의 절대 경로를 알아내어, 상위 폴더 절대 경로를 참조 path에 추가하는 방식입니다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from recommend.views import RecommendFacebook, RecommendNaver
from .config import *
from .forms import *


# Controller Views


class ReportFacebook:
    def send_report(self):
        '''
        '''
        contents = RecommendFacebook().recommend_for_report()
        for content in contents:
            self.send_mail(content)

        print("send_report done: {}".format(datetime.datetime.now()))
        return contents

    def send_mail(self, content):
        '''
        '''
        if not content['facebook']['ads']:
            return print("No ads data of Facebook: {}".format(datetime.datetime.now()))

        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(MAIL['login_id'], MAIL['login_pw'])
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Diana Facebook Report on {}'.format((datetime.datetime.now(
        ) - datetime.timedelta(days=FETCH['from_days'])).strftime('%Y-%m-%d'))
        msg['From'] = MAIL['from']
        recipients = content['user_email']
        msg['To'] = ','.join(recipients)
        html = create_mail_facebook(content)

        if not html:
            print(content)
            print("send_mail failed: {}".format(datetime.datetime.now()))
            return content
        
        msg.attach(MIMEText(html, 'html'))
        smtp.sendmail(msg['From'], recipients, msg.as_string())
        smtp.quit()

        print("send_mail done: {}".format(datetime.datetime.now()))
        return content


class ReportNaver:
    def send_report(self):
        '''
        '''
        contents = RecommendNaver().recommend_for_report()
        for content in contents:
            self.send_mail(content)

        print("send_report done: {}".format(datetime.datetime.now()))
        return contents

    def send_mail(self, content):
        '''
        '''
        if not content['naver']['campaigns']:
            return print("No campaigns data of Naver: {}".format(datetime.datetime.now()))

        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(MAIL['login_id'], MAIL['login_pw'])
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Diana Naver Report on {}'.format((datetime.datetime.now(
        ) - datetime.timedelta(days=FETCH['from_days'])).strftime('%Y-%m-%d'))
        msg['From'] = MAIL['from']
        recipients = content['user_email']
        msg['To'] = ','.join(recipients)
        html = create_mail_naver(content)

        if not html:
            print(content)
            print("send_mail failed: {}".format(datetime.datetime.now()))
            return content

        msg.attach(MIMEText(html, 'html'))
        smtp.sendmail(msg['From'], recipients, msg.as_string())
        smtp.quit()

        print("send_mail done: {}".format(datetime.datetime.now()))
        return content
