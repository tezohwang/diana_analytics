from django.shortcuts import render

from .database import connect_db
from .config import *

import datetime
import json
import numpy


# Controller Views


class RecommendFacebook:
    '''
    generate recommendations for Facebook ads
    '''

    def __init__(self):
        self.db = connect_db('diana')
        self.fbadaccounts = self.db['fbadaccounts']
        self.fbads = self.db['fbads']
        self.fbinsights = self.db['fbinsights']
        self.contents = []
        self.content = {}

    def recommend_for_report(self):
        users = list(self.db['userinfo'].find())
        for user in users:
            self.content = {
                "user_id": user['user_id'],
                "network_id": user['network_id'],
                "username": user['username'],
                "email": user['email'],
                "facebook": {
                    "adaccounts": [],
                    "ads": [],
                    "recos": [],
                },
                "lang": 'en',
            }

            # long access token expiry check
            # if long access token will be expired within 7 days

            adaccounts = self.get_adaccounts()
            # print(adaccounts)

            for adaccount in adaccounts:
                ads = self.get_ads(adaccount)

                if ads:
                    for ad in ads:
                        self.recommend_ad(ad)

            self.contents.append(self.content)
            # print(self.content)

        print(self.contents)
        print("recommend_for_report done: {}".format(datetime.datetime.now()))
        return self.contents

    def get_adaccounts(self):
        adaccounts = list(self.fbadaccounts.find(
            {"network_id": self.content['network_id']}
        ))
        # content['facebook']['adaccounts'] += adaccounts
        return adaccounts

    def get_ads(self, adaccount):
        ads = list(self.fbads.find(
            {
                "account_id": adaccount['account_id'],
                "yesterday.spend": {"$gt": 0},
            }
        ))
        self.content['facebook']['ads'] += ads
        return ads

    def recommend_ad(self, ad):
        data_7days = list(self.fbinsights.find(
            {
                "ad_id": ad['ad_id'],
                "publisher_platform": "facebook",
                "date_stop": {"$gte": datetime.datetime.now() - datetime.timedelta(days=7)}
            }
        ))[-7:]

        # for yesterday
        if len(data_7days) >= 1:
            data = data_7days[-1:]
            self.ctr_check(data)
            self.limit_check(data)
            print("yesterday check done")

        # for at most last 7days
        if len(data_7days) >= 3:
            data = data_7days[-3:]
            self.frequency_check(data)
            print("last 7days check done")

        # for at least last 3days
        if len(data_7days) >= 3:
            data = data_7days[-3:]
            self.spend_check(data)
            self.cpm_check(data)
            self.cpc_check(data)
            self.relevance_score_check(data)
            print("last 3days check done")

        print("recommend_ad done: {}".format(datetime.datetime.now()))
        return self.content

    def ctr_check(self, data):
        score = 0
        if 'relevance_score' in data[0]:
            if 'score' in data[0]['relevance_score']:
                score = int(data[0]['relevance_score']['score'])
        ctr = round(float(data[0]['ctr']), 2)
        if 'inline_link_click_ctr' in data[0]:
            bound_clicks_ctr = round(
                float(data[0]['inline_link_click_ctr']), 2)
        if 'outbound_clicks_ctr' in data[0]:
            bound_clicks_ctr = round(
                float(data[0]['outbound_clicks_ctr'][0]['value']), 2)

        if ctr < CONDITIONS['ctr'] and score <= 5:
            # 전체 클릭률 4% 이하이고, 관련성 점수가 5 이하일 때,
            reco = RECOS[self.content['lang']]['ctr_bad']
            self.append_reco(reco)
        else:
            if bound_clicks_ctr < CONDITIONS['bound_clicks_ctr'] and score <= 5:
                # 바운드 클릭률 2% 이하이고, 관련성 점수가 5 이하이면,
                if data[0]['canvas_avg_view_percent']:
                    # 캔버스 기능이 있으면,
                    reco = RECOS[self.content['lang']
                                 ]['bound_clicks_ctr_bad_with_canvas']
                    self.append_reco(reco)
                    return self.content
                # 캔버스가 없으면,
                reco = RECOS[self.content['lang']
                             ]['bound_clicks_ctr_bad_no_canvas']
                self.append_reco(reco)

        print("ctr_check done: {}".format(datetime.datetime.now()))
        return self.content

    def limit_check(self, data):
        pass

    def frequency_check(self, data):
        pass

    def spend_check(self, data):
        pass

    def cpm_check(self, data):
        pass

    def cpc_check(self, data):
        pass

    def relevance_score_check(self, data):
        pass

    def append_reco(self, reco):
        recos = self.content['facebook']['recos']
        if not reco in recos:
            recos.append(reco)
        return self.content

    def update_recommendations(self):
        pass


class RecommendNaver:
    '''
    generate recommendations for daily report
    '''

    def __init__(self):
        self.db = connect_db('diana')
        self.nvkeywords = self.db['nvkeywords']
        self.nvaccounts = self.db['nvaccounts']

    def recommend_for_report(self):
        autobid_db = connect_db('autobidding')
        users = list(autobid_db['users'].find())

        # # 다이아나 members & sign up 프로세스 완성되면 추가 적용
        # db = connect_db('diana')
        # users = list(db['users'].find(
        # 	{"type": "naver"},
        # ))
        # members = db['members']
        # contents = []
        # for user in users:
        # 	user_email = members.find_one(
        # 		{"user_id": user['user_id']}
        # 	)['email']

        contents = []
        for user in users:
            customer_id = str(user['customer_id'])
            user_email = ['tony.hwang@wizpace.com']
            content = {
                "customer_id": customer_id,
                "username": user['user_id'],
                "user_email": user_email,
                "naver": {},
            }
            self.fetch_by_customer_id(content)

            if 'campaigns' in content['naver']:
                content['naver']['campaigns'] = sorted(
                    content['naver']['campaigns'], key=lambda campaign: campaign['name'])
            if 'adgroups' in content['naver']:
                content['naver']['adgroups'] = sorted(
                    content['naver']['adgroups'], key=lambda adgroup: adgroup['name'])
            self.recommend_entity(content)
            contents.append(content)

        print("recommend_for_report done: {}".format(datetime.datetime.now()))
        return contents

    def fetch_by_customer_id(self, content):
        '''
        fetch campaign & adgroup data from DB by customer_id
        '''

        # 오늘 status가 ELIGIBLE(ON)인 캠페인들
        campaigns_on_today = list(self.db['nvcampaigns'].find(
            {
                "customer_id": content['customer_id'],
                "status": "ELIGIBLE",
            }
        ))
        if campaigns_on_today:
            content['naver']['campaigns'] = campaigns_on_today

        # 오늘 status가 ELIGIBLE(ON), 어제 stat이 있는 광고그룹들
        adgroups_on_today = list(self.db['nvadgroups'].find(
            {
                "customer_id": content['customer_id'],
                "status": "ELIGIBLE",
                "status_reason": "ELIGIBLE",
                "yesterday": {'$ne': {}}
            }
        ))
        if adgroups_on_today:
            content['naver']['adgroups'] = adgroups_on_today

        print("fetch_naver_data done: {}".format(datetime.datetime.now()))
        return content

    def recommend_entity(self, content):
        '''
        '''
        content['naver']['recos'] = []

        # 현재까지 1000원 이상 사용한 키워드 리스트
        keyword_list = list(self.nvkeywords.find(
            {
                'customer_id': content['customer_id'],
                'last_month.spend': {'$gte': THRESHOLD['spend'][content['username']]},
            },
        ))

        for keyword in keyword_list:
            self.recommend_keyword(content, keyword)

        print("recommend_entity done: {}".format(datetime.datetime.now()))
        return content

    def recommend_keyword(self, content, keyword):
        '''
        '''
        # 7일전부터 어제까지의 데이터
        data_7days = list(self.nvstats.find(
            {
                'res_id': keyword['keyword_id'],
                'type': 'keyword',
                'date_end': {'$gte': (datetime.datetime.now() - datetime.timedelta(days=7))}
            }
        ))
        # 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
        sum_ccnts = sum([data['ccnt']
                         for data in data_7days if 'ccnt' in data])
        sum_spends = sum([data['spend']
                          for data in data_7days if 'spend' in data])
        if sum_ccnts == 0 and sum_spends >= THRESHOLD['no_ccnt_spend'][content['username']]:
            content['naver']['recos'].append(
                {
                    'keyword_id': keyword['keyword_id'],
                    'name': keyword['name'],
                    'reco': '7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.'.format(sum_spends, ','),
                }
            )
        # 지난 7일간 CPC 대비 CTR이 가장 좋은 순위를 추천
        ctr_by_cpc = []
        for data in data_7days:
            if 'ctr' in data and 'cpc' in data:
                if data['ctr'] * data['cpc']:
                    ctr_by_cpc.append(data['ctr']/data['cpc'])
        if ctr_by_cpc:
            max_index = ctr_by_cpc.index(max(ctr_by_cpc))
            best_rank = data_7days[max_index]['average_rank']
            if best_rank:
                content['naver']['recos'].append(
                    {
                        'keyword_id': keyword['keyword_id'],
                        'name': keyword['name'],
                        'reco': '7일간 최적 효율 순위는 {}위 입니다'.format(best_rank),
                    }
                )
        # 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배 이상)한 키워드 검출 (CPC가 0인 데이터는 제외)
        if data_7days:
            cpc_for_7days = []
            for data in data_7days:
                if 'cpc' in data:
                    if data['cpc']:
                        cpc_for_7days.append(data['cpc'])
            avg_cpc_for_7days = numpy.mean(cpc_for_7days)

            if all([avg_cpc_for_7days, 'cpc' in data_7days[-1]]):
                if data_7days[-1]['cpc'] > avg_cpc_for_7days * THRESHOLD['avg_cpc_times'][content['username']]:
                    content['naver']['recos'].append(
                        {
                            'keyword_id': keyword['keyword_id'],
                            'name': keyword['name'],
                            'reco': '7일간 평균({}원)에 비해 CPC({}원)가 급상승 했습니다'.format(round(avg_cpc_for_7days, 2), data_7days[-1]['cpc']),
                        }
                    )
        # 지난 7일간 평균 CPM 대비 어제 CPM이 급상승(2배 이상)한 키워드 검출 (CPM이 0인 데이터는 제외)
        if data_7days:
            cpm_for_7days = []
            for data in data_7days:
                if 'impressions' in data and 'spend' in data:
                    if data['impressions'] * data['spend']:
                        cpm_for_7days.append(data['spend']/data['impressions'])
            avg_cpm_for_7days = numpy.mean(cpm_for_7days)

            if all([avg_cpm_for_7days, 'spend' in data_7days[-1], 'impressions' in data_7days[-1]]):
                if data_7days[-1]['spend']/data_7days[-1]['impressions'] > avg_cpm_for_7days * THRESHOLD['avg_cpm_times'][content['username']]:
                    content['naver']['recos'].append(
                        {
                            'keyword_id': keyword['keyword_id'],
                            'name': keyword['name'],
                            'reco': '7일간 평균({}원)에 비해 노출 경쟁(CPM, {}원)이 급상승 했습니다'.format(round(avg_cpm_for_7days, 2), round(data_7days[-1]['spend']/data_7days[-1]['impressions'], 2)),
                        }
                    )
        # 지난 7일간 평균 Impressions 대비 어제 Impressions 급상승(2배 이상)한 키워드 검출 (Impressions이 0인 데이터는 제외)
        if data_7days:
            imp_for_7days = []
            for data in data_7days:
                if 'impressions' in data:
                    if data['impressions']:
                        imp_for_7days.append(data['impressions'])
            avg_imp_for_7days = numpy.mean(imp_for_7days)

            if all([avg_imp_for_7days, 'impressions' in data_7days[-1]]):
                if data_7days[-1]['impressions'] > avg_imp_for_7days * THRESHOLD['avg_imp_times'][content['username']]:
                    content['naver']['recos'].append(
                        {
                            'keyword_id': keyword['keyword_id'],
                            'name': keyword['name'],
                            'reco': '7일간 평균({}회)에 비해 노출({}회)이 급상승 했습니다'.format(round(avg_imp_for_7days, 2), data_7days[-1]['impressions']),
                        }
                    )

        print("recommend_keyword done: {}".format(datetime.datetime.now()))
        return content

    def update_recommendations(self):
        '''
        update recommendations of every keyword with data of 7days and yesterday
        '''
        keyword_list = self.nvkeywords.find({"status": "ELIGIBLE"})

        for keyword in keyword_list:
            print("Keyword: {}".format(keyword['name']))

            recos = []
            username = self.nvaccounts.find_one({"client_customer_id": keyword['customer_id']})[
                'client_login_id']
            last_week = keyword['last_week']
            yesterday = keyword['yesterday']

            # 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
            if last_week['ccnt'] == 0 and last_week['spend'] >= THRESHOLD['no_ccnt_spend'][username]:
                reco = "7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.".format(
                    format(last_week['spend'], ','))
                recos.append(reco)

            # 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배 이상)한 키워드 검출 (CPC가 0인 데이터는 제외)
            if yesterday['cpc'] > last_week['cpc'] * THRESHOLD['avg_cpc_times'][username]:
                last_week_cpc = format(round(last_week['cpc']), ',')
                yesterday_cpc = format(round(yesterday['cpc']), ',')
                reco = "7일간 평균({}원) 대비 1일 전 CPC({}원)가 급상승했습니다.".format(
                    last_week_cpc, yesterday_cpc)
                recos.append(reco)

            # 지난 7일간 평균 CPM 대비 어제 CPM이 급상승(2배 이상)한 키워드 검출 (CPM이 0인 데이터는 제외)
            if yesterday['cpm'] > last_week['cpm'] * THRESHOLD['avg_cpc_times'][username]:
                last_week_cpm = format(round(last_week['cpm']), ',')
                yesterday_cpm = format(round(yesterday['cpm']), ',')
                reco = "7일간 평균({}원) 대비 1일 전 CPM({}원)이 급상승했습니다.".format(
                    last_week_cpm, yesterday_cpm)
                recos.append(reco)

            # 지난 7일간 평균 Impressions 대비 어제 Impressions 급상승(2배 이상)한 키워드 검출 (Impressions이 0인 데이터는 제외)
            if yesterday['impressions'] > last_week['impressions'] * THRESHOLD['avg_cpc_times'][username]:
                last_week_imp = format(round(last_week['impressions']), ',')
                yesterday_imp = format(round(yesterday['impressions']), ',')
                reco = "7일간 평균({}회) 대비 1일 전 노출({}회)이 급상승했습니다.".format(
                    last_week_imp, yesterday_imp)
                recos.append(reco)

            # update recos for each keyword
            self.nvkeywords.update_one(
                {"keyword_id": keyword['keyword_id']},
                {"$set": {"recommendation": recos}}
            )

        print("update_recommendations done: {}".format(datetime.datetime.now()))
        return recos
