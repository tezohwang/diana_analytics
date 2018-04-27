from django.shortcuts import render

import os
import sys
# 현재 모듈의 절대 경로를 알아내어, 상위 폴더 절대 경로를 참조 path에 추가하는 방식입니다.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from recommend.views import RecommendNaver

# Facebook
class ReportFacebook:
    pass

# Naver
class ReportNaver:
    def send_report(self):
        contents = RecommendNaver().recommend_for_report()
        print(contents)


# Adwords


ReportNaver().send_report()