from django.shortcuts import render

from .database import connect_db

import datetime
import json
import numpy


# Controller Views

# FACEBOOK


# NAVER
def update_recommendations():
    db = connect_db('diana')
    nvkeywords = db['nvkeywords']
    nvaccounts = db['nvaccounts']
    keyword_list = nvkeywords.find({"status": "ELIGIBLE"})

    for keyword in keyword_list:
        print("Keyword: {}".format(keyword['name']))

        recos = []
        username = nvaccounts.find_one({"client_customer_id": keyword['customer_id']})[
            'client_login_id']
        last_week = keyword['last_week']
        yesterday = keyword['yesterday']

        # 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
        if last_week['ccnt'] == 0 and last_week['spend'] >= RECOMMEND['no_ccnt_spend'][username]:
            reco = "7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.".format(
                format(last_week['spend'], ','))
            recos.append(reco)

        # 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배 이상)한 키워드 검출 (CPC가 0인 데이터는 제외)
        if yesterday['cpc'] > last_week['cpc'] * RECOMMEND['avg_cpc_times'][username]:
            last_week_cpc = format(round(last_week['cpc']), ',')
            yesterday_cpc = format(round(yesterday['cpc']), ',')
            reco = "7일간 평균({}원) 대비 1일 전 CPC({}원)가 급상승했습니다.".format(
                last_week_cpc, yesterday_cpc)
            recos.append(reco)

        # 지난 7일간 평균 CPM 대비 어제 CPM이 급상승(2배 이상)한 키워드 검출 (CPM이 0인 데이터는 제외)
        if yesterday['cpm'] > last_week['cpm'] * RECOMMEND['avg_cpc_times'][username]:
            last_week_cpm = format(round(last_week['cpm']), ',')
            yesterday_cpm = format(round(yesterday['cpm']), ',')
            reco = "7일간 평균({}원) 대비 1일 전 CPM({}원)이 급상승했습니다.".format(
                last_week_cpm, yesterday_cpm)
            recos.append(reco)

        # 지난 7일간 평균 Impressions 대비 어제 Impressions 급상승(2배 이상)한 키워드 검출 (Impressions이 0인 데이터는 제외)
        if yesterday['impressions'] > last_week['impressions'] * RECOMMEND['avg_cpc_times'][username]:
            last_week_imp = format(round(last_week['impressions']), ',')
            yesterday_imp = format(round(yesterday['impressions']), ',')
            reco = "7일간 평균({}회) 대비 1일 전 노출({}회)이 급상승했습니다.".format(
                last_week_imp, yesterday_imp)
            recos.append(reco)

		# update recos for each keyword
        nvkeywords.update_one(
            {"keyword_id": keyword['keyword_id']},
            {"$set": {"recommendation": recos}}
        )
        print(recos)

    return print("update_recommendations done: {}".format(datetime.datetime.now()))

# ADWORDS
