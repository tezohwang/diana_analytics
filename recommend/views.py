from django.shortcuts import render

from .database import connect_db
from .config import *

import datetime
import json
import numpy as np


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
                    # "adaccounts": [],
                    "ads": [],
                },
                "lang": 'en',
            }

            # long access token expiry check
            # if long access token will be expired within 7 days

            adaccounts = self.get_adaccounts()

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
        ad['recos'] = []
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
            self.ctr_check(data, ad)
            self.limit_check(data, ad)
            print("yesterday check done")

        # for at most last 7days
        if len(data_7days) >= 3:
            data = data_7days[-7:]
            self.frequency_check(data, ad)
            print("last 7days check done")

        # for at least last 3days
        if len(data_7days) >= 2:
            data = data_7days[-3:]
            self.spend_check(data, ad)
            self.cpm_check(data, ad)
            self.cpc_check(data, ad)
            self.relevance_score_check(data, ad)
            print("last 3days check done")

        print("recommend_ad done: {}".format(datetime.datetime.now()))
        return ad['recos']

    def ctr_check(self, data, ad):
        score = 0
        if 'relevance_score' in data[0]:
            if 'score' in data[0]['relevance_score']:
                score = int(data[0]['relevance_score']['score'])
        ctr = round(data[0]['ctr'], 2)
        bound_clicks_ctr = 0
        if 'inline_link_click_ctr' in data[0]:
            bound_clicks_ctr = round(
                data[0]['inline_link_click_ctr'], 2)
        if 'outbound_clicks_ctr' in data[0]:
            bound_clicks_ctr = round(
                data[0]['outbound_clicks_ctr'][0]['value'], 2)

        if ctr < CONDITIONS['ctr'] and score <= 5:
            # 전체 클릭률 4% 이하이고, 관련성 점수가 5 이하일 때,
            reco = RECOS[self.content['lang']]['ctr_bad']
            self.append_reco(reco, ad)

        if bound_clicks_ctr:
            if bound_clicks_ctr < CONDITIONS['bound_clicks_ctr'] and score <= 5:
                # 바운드 클릭률 2% 이하이고, 관련성 점수가 5 이하이면,
                if data[0]['canvas_avg_view_percent']:
                    # 캔버스 기능이 있으면,
                    reco = RECOS[self.content['lang']
                                 ]['bound_clicks_ctr_bad_with_canvas']
                    self.append_reco(reco, ad)
                    return self.content
                # 캔버스가 없으면,
                reco = RECOS[self.content['lang']
                             ]['bound_clicks_ctr_bad_no_canvas']
                self.append_reco(reco, ad)

        print("ctr_check done: {}".format(datetime.datetime.now()))
        return self.content

    def limit_check(self, data, ad):
        cpm = data[0]['cpm']
        if cpm > CONDITIONS['cpm_limit']:
            reco = RECOS[self.content['lang']]['cpm_limit']
            self.append_reco(reco, ad)

        print("limit_check done: {}".format(datetime.datetime.now()))
        return self.content

    def frequency_check(self, data, ad):
        frequencies = [_data['frequency'] for _data in data]
        avg_frequency = np.mean(frequencies)

        if avg_frequency > CONDITIONS['frequency_limit']:
            reco = RECOS[self.content['lang']]['frequency_limit']
            self.append_reco(reco, ad)

        print("frequency_check done: {}".format(datetime.datetime.now()))
        return self.content

    def spend_check(self, data, ad):
        spends = [_data['spend'] for _data in data]

        # 전날 대비 지출의 급격한 상승 체크
        if spends[-1] >= spends[-2] * CONDITIONS['spend_times_for_boom'] and spends[-1] >= CONDITIONS['spend_min_for_check']:
            reco = RECOS[self.content['lang']]['spend_boom']
            self.append_reco(reco, ad)

        # 지출 급격한 변화 체크에는 최소 3일간 데이터가 필요
        if len(spends) < CONDITIONS['spend_length']:
            print("not enough spends data: {}".format(len(spends)))
            return self.content

        avg_spend = np.mean(spends)
        std_spend = np.std(spends)

        # 평균과 지출의 변화 정도를 비교
        if std_spend > avg_spend:
            # 지출의 변동이 심하면, (평균 이상이면)
            if spends[-3] > spends[-2] and spends[-2] > spends[-1]:
                reco = RECOS[self.content['lang']]['spend_down']
            elif spends[-3] < spends[-2] and spends[-2] < spends[-1]:
                reco = RECOS[self.content['lang']]['spend_up']
            else:
                reco = RECOS[self.content['lang']]['spend_unstable']
            self.append_reco(reco, ad)

        print("spend_check done: {}".format(datetime.datetime.now()))
        return self.content

    def cpm_check(self, data, ad):
        cpms = [_data['cpm'] for _data in data]

        if len(cpms) < CONDITIONS['cpm_length']:
            print("not enough cpms data: {}".format(len(cpms)))
            return self.content

        avg_cpm = np.mean(cpms)

        for cpm in cpms:
            # 하루 cpm이 최근 n일간 cpm 평균의 1.5배를 넘으면,
            if cpm > avg_cpm * CONDITIONS['cpm_avg_limit']:
                reco = RECOS[self.content['lang']]['cpm_avg_limit']
                self.append_reco(reco, ad)
            # 가장 최근일의 cpm이 cpm 평균의 2.0배를 넘으면,
            elif cpms[-1] > avg_cpm * CONDITIONS['cpm_limit']:
                reco = RECOS[self.content['lang']]['cpm_limit']
                self.append_reco(reco, ad)
            else:
                pass

        print("cpm_check done: {}".format(datetime.datetime.now()))
        return self.content

    def cpc_check(self, data, ad):
        cpcs = [_data['cost_per_inline_link_click'] for _data in data]

        if len(cpcs) < CONDITIONS['cpc_length']:
            print("not enough cpcs data: {}".format(len(cpcs)))
            return self.content

        avg_cpc = np.mean(cpcs)

        # 지출은 있으나, 모든 cpc가 0일 경우 = 링크 클릭이 발생하지 않을 경우,
        if not any(cpcs):
            reco = str(len(cpcs)) + \
                RECOS[self.content['lang']]['no_link_click']
            self.append_reco(reco, ad)
        else:
            # 가장 최근일의 cpm이 cpm 평균의 2.0배를 넘으면,
            if cpcs[-1] > avg_cpc * CONDITIONS['cpc_limit']:
                reco = RECOS[self.content['lang']]['cpc_limit']
                self.append_reco(reco, ad)

        print("cpc_check done: {}".format(datetime.datetime.now()))
        return self.content

    def relevance_score_check(self, data, ad):
        if 'relevance_score' in data[-1]:
            if 'score' in data[-1]['relevance_score']:
                relevance_score = data[-1]['relevance_score']['score']
                if relevance_score in ['1', '2', '3']:
                    reco = RECOS[self.content['lang']]['relevance_score']
                    self.append_reco(reco, ad)

        print("relevance_score_check done: {}".format(datetime.datetime.now()))
        return self.content

    def append_reco(self, reco, ad):
        recos = ad['recos']
        if not reco in recos:
            recos.append(reco)
        return ad

    def get_lang(self, adaccount):
        lang = 'en'
        if adaccount['currency'] == 'KRW':
            lang = 'kr'
        return lang

    def update_recommendations(self):
        '''
        update recommendations of every keyword with data of 7days and yesterday
        '''
        self.content = {
            "facebook": {
                "recos": [],
            },
            "lang": 'en',
        }

        # 지난 1주일 동안 0원 이상 사용했던 ads 리스트
        ads = self.fbads.find({"last_week.spend": {"$gt": 0}})
        for ad in ads:
            adaccount = self.fbadaccounts.find_one(
                {"account_id": ad['account_id']})
            self.content['lang'] = self.get_lang(adaccount)
            recos = self.recommend_ad(ad)
            self.fbads.update_one(
                {"ad_id": ad['ad_id']},
                {"$set": {"recommendation": recos}}
            )
        print("update_recommendations done: {}".format(datetime.datetime.now()))
        return recos


class RecommendNaver:
    '''
    generate recommendations for daily report
    '''

    def __init__(self):
        self.db = connect_db('diana')
        self.nvkeywords = self.db['nvkeywords']
        self.nvaccounts = self.db['nvaccounts']
        self.nvstats = self.db['nvstats']
        self.contents = []
        self.content = {}

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

        for user in users:
            customer_id = str(user['customer_id'])
            user_email = ['tony.hwang@wizpace.com']
            self.content = {
                "customer_id": customer_id,
                "username": user['user_id'],
                "user_email": user_email,
                "naver": {
                    "campaigns": [],
                    "adgroups": [],
                },
            }
            self.fetch_by_customer_id()

            if self.content['naver']['campaigns']:
                campaigns = self.content['naver']['campaigns']
                campaigns = sorted(
                    campaigns, key=lambda campaign: campaign['name'])

            if self.content['naver']['adgroups']:
                adgroups = self.content['naver']['adgroups']
                adgroups = sorted(
                    adgroups, key=lambda adgroup: adgroup['name'])
            self.recommend_entity()
            self.contents.append(self.content)

        print(self.contents)
        print("recommend_for_report done: {}".format(datetime.datetime.now()))
        return self.contents

    def fetch_by_customer_id(self):
        '''
        fetch campaign & adgroup data from DB by customer_id
        '''

        # 오늘 status가 ELIGIBLE(ON)인 캠페인들
        campaigns_on_today = list(self.db['nvcampaigns'].find(
            {
                "customer_id": self.content['customer_id'],
                "status": "ELIGIBLE",
            }
        ))
        if campaigns_on_today:
            self.content['naver']['campaigns'] = campaigns_on_today

        # 오늘 status가 ELIGIBLE(ON), 어제 stat이 있는 광고그룹들
        adgroups_on_today = list(self.db['nvadgroups'].find(
            {
                "customer_id": self.content['customer_id'],
                "status": "ELIGIBLE",
                "status_reason": "ELIGIBLE",
                "yesterday": {'$ne': {}}
            }
        ))
        if adgroups_on_today:
            self.content['naver']['adgroups'] = adgroups_on_today

        print("fetch_naver_data done: {}".format(datetime.datetime.now()))
        return self.content

    def recommend_entity(self):
        '''
        '''
        self.content['naver']['recos'] = []

        # 현재까지 1000원 이상 사용한 키워드 리스트
        keyword_list = list(self.nvkeywords.find(
            {
                'customer_id': self.content['customer_id'],
                'last_month.spend': {'$gte': THRESHOLD['spend'][self.content['username']]},
            },
        ))

        for keyword in keyword_list:
            self.recommend_keyword(keyword)

        print("recommend_entity done: {}".format(datetime.datetime.now()))
        return self.content

    def recommend_keyword(self, keyword):
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
        if sum_ccnts == 0 and sum_spends >= THRESHOLD['no_ccnt_spend'][self.content['username']]:
            self.content['naver']['recos'].append(
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
                self.content['naver']['recos'].append(
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
            avg_cpc_for_7days = np.mean(cpc_for_7days)

            if all([avg_cpc_for_7days, 'cpc' in data_7days[-1]]):
                if data_7days[-1]['cpc'] > avg_cpc_for_7days * THRESHOLD['avg_cpc_times'][self.content['username']]:
                    self.content['naver']['recos'].append(
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
            avg_cpm_for_7days = np.mean(cpm_for_7days)

            if all([avg_cpm_for_7days, 'spend' in data_7days[-1], 'impressions' in data_7days[-1]]):
                if data_7days[-1]['spend']/data_7days[-1]['impressions'] > avg_cpm_for_7days * THRESHOLD['avg_cpm_times'][self.content['username']]:
                    self.content['naver']['recos'].append(
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
            avg_imp_for_7days = np.mean(imp_for_7days)

            if all([avg_imp_for_7days, 'impressions' in data_7days[-1]]):
                if data_7days[-1]['impressions'] > avg_imp_for_7days * THRESHOLD['avg_imp_times'][self.content['username']]:
                    self.content['naver']['recos'].append(
                        {
                            'keyword_id': keyword['keyword_id'],
                            'name': keyword['name'],
                            'reco': '7일간 평균({}회)에 비해 노출({}회)이 급상승 했습니다'.format(round(avg_imp_for_7days, 2), data_7days[-1]['impressions']),
                        }
                    )

        print("recommend_keyword done: {}".format(datetime.datetime.now()))
        return self.content

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
