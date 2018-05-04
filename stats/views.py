from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .database import connect_db
from .config import *

import datetime
import time
import json
import requests
import numpy as np


# Router Views
@csrf_exempt
def get_stats(request):
    '''
    '''
    if request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))
        if not req:
            return HttpResponse(json.dumps("empty request").encode('utf-8'))

        if not 'entity' in req:
            return HttpResponse(json.dumps("value of 'entity' key is required").encode('utf-8'))
        entity = req['entity']

        breakdown = ''
        objective = ''
        currency = ''
        entity_id = ''
        billing_event = ''
        optimization_goal = ''

        if 'breakdown' in req:
            breakdown = req['breakdown']
        if 'objective' in req:
            objective = req['objective']
        if 'currency' in req:
            currency = req['currency']
        if entity + '_id' in req:
            entity_id = req[entity + '_id']
        if 'billing_event' in req:
            billing_event = req['billing_event']
        if 'optimization_goal' in req:
            optimization_goal = req['optimization_goal']

        db = connect_db('diana')

        for key in RESULT[breakdown].keys():
            print(entity, breakdown, objective, currency, key)
            query_obj = {}
            if breakdown:
                query_obj['breakdowns'] = breakdown
            if objective:
                query_obj['objective'] = objective
            if currency:
                query_obj['account_currency'] = currency
            if entity_id:
                query_obj[entity + '_id'] = entity_id
            if billing_event:
                query_obj['billing_event'] = billing_event
            if optimization_goal:
                query_obj['optimization_goal'] = optimization_goal
            if not breakdown == 'none':
                query_obj[breakdown] = key

            print(query_obj)
            entities = list(db['stats_' + entity].find(query_obj))
            if not entities:
                continue
            if not float(entities[0]['impressions']) * float(entities[0]['clicks']):
                continue

            
            spends = [float(entity['spend'])
                      for entity in entities if 'spend' in entity]
            impressions = [float(entity['impressions'])
                           for entity in entities if 'impressions' in entity]
            reaches = [float(entity['reach'])
                       for entity in entities if 'reach' in entity]
            clicks = [float(entity['clicks'])
                      for entity in entities if 'clicks' in entity]
            inline_link_clicks = [float(entity['inline_link_clicks'])
                                  for entity in entities if 'inline_link_clicks' in entity]
            inline_link_click_ctrs = [float(entity['inline_link_click_ctr'])
                                      for entity in entities if 'inline_link_click_ctr' in entity]
            outbound_clicks = [float(entity['outbound_clicks'][0]['value'])
                               for entity in entities if 'outbound_clicks' in entity]
            outbound_clicks_ctrs = [float(entity['outbound_clicks_ctr'][0]['value'])
                                    for entity in entities if 'outbound_clicks_ctr' in entity]
            cost_per_outbound_clicks = [float(entity['cost_per_outbound_click'][0]['value'])
                                        for entity in entities if 'cost_per_outbound_click' in entity]
            cost_per_inline_link_clicks = [float(entity['cost_per_inline_link_click'])
                                           for entity in entities if 'cost_per_inline_link_click' in entity]
            cost_per_total_actions = [float(entity['cost_per_total_action'])
                                      for entity in entities if 'cost_per_total_action' in entity]
            cpms = [float(entity['cpm'])
                    for entity in entities if 'cpm' in entity]
            cpcs = [float(entity['cpc'])
                    for entity in entities if 'cpc' in entity]
            ctrs = [float(entity['ctr'])
                    for entity in entities if 'ctr' in entity]
            frequencys = [float(entity['frequency'])
                          for entity in entities if 'frequency' in entity]

            RESULT[breakdown][key] = {
                'objective': entities[0]['objective'],
                'avg_cpm': round(sum(spends)/sum(impressions)*1000, 2),
                'avg_cpc': round(sum(spends)/sum(clicks), 2),
                'avg_frequency': round(sum(impressions)/sum(reaches), 2),
                'avg_ctr': round(sum(clicks)/sum(impressions)*100, 2),
                'avg_cost_per_inline_link_click': round(sum(spends)/sum(inline_link_clicks), 2),
                'avg_cost_per_outbount_click': round(sum(spends)/sum(outbound_clicks), 2),
                'med_cpm': round(np.median(cpms), 2),
                'med_cpc': round(np.median(cpcs), 2),
                'med_frequency': round(np.median(frequencys), 2),
                'med_ctr': round(np.median(ctrs), 2),
                'med_cost_per_inline_link_click': round(np.median(cost_per_inline_link_clicks), 2),
                'med_cost_per_outbound_click': round(np.median(cost_per_outbound_clicks), 2),
                'med_cost_per_total_action': round(np.median(cost_per_total_actions), 2),
            }
        RESULT[breakdown]['currency'] = currency
        print(RESULT[breakdown])
        return HttpResponse(json.dumps(RESULT[breakdown]).encode('utf-8'))
    return HttpResponse(json.dumps("error").encode('utf-8'))


# Controller Views
class StatsFacebook:
    '''
    '''

    def __init__(self):
        self.db = connect_db('diana')
        self.fbadaccounts = self.db['fbadaccounts']
        self.fbadcampaigns = self.db['fbadcampaigns']
        self.fbadsets = self.db['fbadsets']
        self.fbads = self.db['fbads']

    def get_users(self):
        # Diana users
        # users = list(self.db['users'].find(
        #     {"type": "facebook"},
        # ))

        # Only users who logged in Report webpage
        users = list(self.db['userinfo'].find())
        return users

    def get_adaccounts(self, user):
        adaccounts = list(self.fbadaccounts.find(
            {"network_id": user['network_id']}
        ))
        return adaccounts

    def get_entities_list(self, user, adaccount, entity_type):
        params = {'date_preset': 'last_30d'}
        url = 'https://graph.facebook.com/v3.0/' + \
            adaccount['ad_account_id'] + '/' + entity_type + \
            's?access_token=' + user['access_token']
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'content-encoding': 'gzip'
        }
        response = requests.get(url, params=params, headers=headers)
        response = response.json()
        print(response)
        if 'error' in response:
            if response['error']['code'] == 3:
                print("Application does not have the capability to make this API call.")
                return []
            if response['error']['code'] == 17:
                print("reach api limit, wait {} seconds and retry".format(
                    TIME['limit_wait_time']))
                time.sleep(TIME['limit_wait_time'])
                response['data'] = self.get_entities_list(user, adaccount, entity_type)
            if response['error']['code'] in [100, 190, 274]:
                # print(response['error']['message'])
                return "break"
        try:
            return response['data']
        except Exception as e:
            return []


    def get_entity_insights(self, user, entity_type, entity, breakdown):
        fields = FIELDS[entity_type]
        params = {
            "fields": str(fields),
            "date_preset": "last_30d",
            "time_increment": "all_days",
            "breakdowns": str(breakdown),
        }
        url = 'https://graph.facebook.com/v3.0/' + \
            entity['id'] + '/insights?access_token=' + user['access_token']
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'content-encoding': 'gzip'
        }
        response = requests.get(url, params=params, headers=headers)
        response = response.json()
        print(response)
        if 'error' in response:
            if response['error']['code'] == 17:
                print("reach api limit, wait {} seconds and retry".format(
                    TIME['limit_wait_time']))
                time.sleep(TIME['limit_wait_time'])
                response['data'] = self.get_entity_insights(
                    user, entity_type, entity, breakdown)
        try:
            return response['data']
        except Exception as e:
            return []

    def update_db(self, entity_type, insights, breakdown):
        collection = self.db['stats_' + entity_type]
        for insight in insights:
            insight['breakdowns'] = breakdown
            if not breakdown:
                insight['breakdowns'] = ['none']
            insight['updated_time'] = datetime.datetime.now()
            collection.replace_one(
                {
                    entity_type + '_id': insight[entity_type + '_id'],
                    "breakdowns": insight['breakdowns'],
                },
                insight,
                upsert=True,
            )
        print("update_db done")
        return insights

    def get_entity_field_values(self, user, adaccount, entity, entity_type):
        params = {"date_preset": "last_30d"}
        if not entity_type == 'adset':
            return []
        params['fields'] = str([
            "id",
            "account_id",
            "campaign_id",
            "name",
            "billing_event",
            "budget_remaining",
            "daily_budget",
            "lifetime_budget",
            "optimization_goal",
        ])
        url = 'https://graph.facebook.com/v3.0/' + \
            entity['id'] + '?access_token=' + user['access_token']
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'content-encoding': 'gzip'
        }
        response = requests.get(url, params=params, headers=headers)
        response = response.json()
        print(response)
        if 'error' in response:
            if response['error']['code'] == 3:
                print("Application does not have the capability to make this API call.")
                return []
            if response['error']['code'] == 17:
                print("reach api limit, wait {} seconds and retry".format(
                    TIME['limit_wait_time']))
                time.sleep(TIME['limit_wait_time'])
                response = self.get_entity_field_values(user, adaccount, entity, entity_type)
        try:
            return response
        except Exception as e:
            return []

    def update_field_values(self, user, field_values, breakdown):
        stats_adset = self.db['stats_adset']
        if not breakdown:
            breakdown = ['none']
        stats_adset.update(
            {
                "adset_id": field_values['id'],
                "breakdowns": breakdown,
            },
            {
                "$set": {
                    "billing_event": field_values['billing_event'],
                    "budget_remaining": field_values['budget_remaining'],
                    "daily_budget": field_values['daily_budget'],
                    "lifetime_budget": field_values['lifetime_budget'],
                    "optimization_goal": field_values['optimization_goal'],
                }
            }
        )
        print("update_field_values done")
        return field_values

    def fetch_stats(self):
        start_time = time.time()
        # ------------------------
        users = self.get_users()

        for user in users:
            adaccounts = self.get_adaccounts(user)
            for breakdown in BREAKDOWNS['facebook']:
                for adaccount in adaccounts:
                    for entity_type in ENTITY_TYPES['facebook']:
                        entities = self.get_entities_list(user, adaccount, entity_type)
                        if entities == "break":
                            break
                        time.sleep(TIME['loop_wait_time'])
                        for entity in entities:
                            insights = self.get_entity_insights(
                                user, entity_type, entity, breakdown)
                            if insights:
                                self.update_db(entity_type, insights, breakdown)
                                time.sleep(TIME['loop_wait_time'])
                                field_values = self.get_entity_field_values(user, adaccount, entity, entity_type)
                                if field_values:
                                    self.update_field_values(user, field_values, breakdown)
        # ------------------------
        print("start_time", start_time)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("fetch_all done: {}".format(datetime.datetime.now()))
        return users
