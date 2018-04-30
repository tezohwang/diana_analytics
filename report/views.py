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

from recommend.views import RecommendNaver
from .config import *
from .forms import *


# Facebook


class ReportFacebook:
	pass

# Naver


class ReportNaver:
	def send_report(self):
		contents = RecommendNaver().recommend_for_report()
		for content in contents:
			self.send_mail(content)

		print("send_report done: {}".format(datetime.datetime.now()))
		return contents

	def send_mail(self, content):
		# 모든 채널에 대한 데이터가 없으면, 메일을 보내지 않는다.
		if not 'naver' in content:
			return print("No data of Naver: {}".format(datetime.datetime.now()))

		if not 'campaigns' in content['naver']:
			return print("No campaigns data of Naver: {}".format(datetime.datetime.now()))

		smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		smtp.login(MAIL['login_id'], MAIL['login_pw'])
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Diana Naver Report on {}'.format((datetime.datetime.now(
		) - datetime.timedelta(days=FETCH['from_days'])).strftime('%Y-%m-%d'))
		msg['From'] = MAIL['from']
		recipients = content['user_email']
		msg['To'] = ','.join(recipients)
		html = create_mail(content)

		if not html:
			print(content)
			print("send_mail failed: {}".format(datetime.datetime.now()))
			return content

		msg.attach(MIMEText(html, 'html'))
		smtp.sendmail(msg['From'], recipients, msg.as_string())
		smtp.quit()

		print("send_mail done: {}".format(datetime.datetime.now()))
		return content


# Adwords
