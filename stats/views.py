from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .database import connect_db
from .config import *

import datetime
import json
import numpy as np


# Controller Views
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
