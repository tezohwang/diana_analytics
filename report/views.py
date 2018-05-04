from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import sys
# 현재 모듈의 절대 경로를 알아내어, 상위 폴더 절대 경로를 참조 path에 추가하는 방식입니다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import json
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from recommend.views import RecommendFacebook, RecommendNaver
from .config import *
from .forms import *


# Route Views
@csrf_exempt
def send_mail(request):
    if request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))

        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(MAIL['login_id'], MAIL['login_pw'])
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Diana Email Service'
        msg['From'] = MAIL['from']
        recipients = MAIL['recipients']
        msg['To'] = ','.join(recipients)

        html = ""
        for key in req.keys():
            html += "<p>{}: {}</p>".format(key, req[key])

        msg.attach(MIMEText(html, 'html'))
        smtp.sendmail(msg['From'], recipients, msg.as_string())
        smtp.quit()

        print(html)
        print("send_mail done: {}".format(datetime.datetime.now()))

        return HttpResponse(json.dumps("success").encode('utf-8'))
    return HttpResponse(json.dumps("error").encode('utf-8'))


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
        recipients = content['user_email'] + MAIL['recipients']
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
        recipients = content['user_email'] + MAIL['recipients']
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
