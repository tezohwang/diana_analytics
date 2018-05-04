DATABASE = {
    "diana": {
        "uri": "mongodb://wizpace:wizpace0@13.125.239.144:27017/diana",
        "name": "diana"
    },
    "autobidding": {
        "uri": "mongodb://autobidding:autobid0@13.125.87.196:27017/autobidding",
        "name": "autobidding"
    }
}

BREAKDOWNS = {
    "facebook": [
        ['age'],
        ['gender'],
        ['country'],
        ['publisher_platform'],
        [],
    ],
}

ENTITY_TYPES = {
    "facebook": [
        'campaign',
        'adset',
        'ad',
    ],
}

TIME = {
    'loop_wait_time': 1.0,
    'limit_wait_time': 310,
}

FIELDS = {
    'campaign': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
    'adset': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'adset_id',
        'adset_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
    'ad': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'adset_id',
        'adset_name',
        'ad_id',
        'ad_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
}

RESULT = {
    'age': {
        '13-17': {},
        '18-24': {},
        '25-34': {},
        '35-44': {},
        '45-54': {},
        '55-64': {},
        '65+': {},
    },
    'gender': {
        'male': {},
        'female': {},
    },
    'country': {
        'US': {},
        'KR': {},
        'MX': {},
        'PE': {},
        'RO': {},
        'DZ': {},
        'GD': {},
    },
    'publisher_platform': {
        'facebook': {},
        'instagram': {},
        'messenger': {},
        'audience_network': {},
    },
    'none': {
        'data': {},
    },
}
