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

CLIENTS = {
    "facebook": [],
    "naver": [
        "bestgo",
        "baronmotors",
        "uiseong",
        "wizpace",
        "ponitto",
    ],
    "adwords": [],
}

THRESHOLD = {
    "spend": {
        "default": 500000,
        "bestgo": 500000,
        "baronmotors": 500000,
        "uiseong": 3000,
        "wizpace": 1500,
        "ponitto": 50000,
    },
    'no_ccnt_spend': {
        "default": 50000,
        "bestgo": 50000,
        "baronmotors": 50000,
        "uiseong": 1000,
        "wizpace": 500,
        "ponitto": 5000,
    },
    'avg_cpc_times': {
        "default": 3.0,
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
        "ponitto": 2.0,
    },
    'avg_cpm_times': {
        "default": 3.0,
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
        "ponitto": 2.0,
    },
    'avg_imp_times': {
        "default": 3.0,
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
        "ponitto": 2.0,
    },
}

CONDITIONS = {
    'frequency_limit': 1.8,
    'spend_length': 3,
    'spend_times_for_boom': 3,
    'spend_min_for_check': 10000,
    'cpm_length': 3,
    'cpm_avg_limit': 1.5,
    'cpm_limit': 2.0,
    'cpc_length': 3,
    'cpc_limit': 400,
    'ctr': 2.0,
    'bound_clicks_ctr': 2.00,
}

RECOS = {
    'en': {
        'frequency_limit': 'frequency of within last 7 days has been over the limit({}). For avoiding redundancy, expand your target or pause this ad for a while.'.format(CONDITIONS['frequency_limit']),
        'spend_boom': "Spend incresed {} times more for a day. Please take care this ad.".format(CONDITIONS['spend_times_for_boom']),
        'spend_down': "Spending rate decreased too much. Expand your target size, or stop this ad.",
        'spend_up': "Spending rate increased dramatically. Narrow down target size or time periods of this ad.",
        'spend_unstable': "Spending rate is unstable. Check your target size or time periods of this ad.",
        'cpm_avg_limit': "CPM increased too much of a specific day. Adjust optimization_goal or target settings of the adset of this ad.",
        'cpm_limit': "CPM has been over the limit. Adjust optimization_goal or target settings of the adset of this ad.",
        'no_link_click': " days with no link click. Change target settings or stop this ad.",
        'cpc_limit': "CPC(Link click) has been over the limit. Change target settings or stop this ad.",
        'ctr_bad': "Reactions(CTR) of this ad was bad. Adjust or change creatives(image, video, ad format) of this ad.",
        'bound_clicks_ctr_bad_with_canvas': "Customer's outbound rate was low. Subdivide target with specific breakdowns(Gender, Age, Platform).",
        'bound_clicks_ctr_bad_no_canvas': "Customer's outbound rate was low. Utilize the canvas format for an inducing step.",
        'relevance_score': 'Relevance score is too low. Please improve creatives(image, video, ad format) of this ad.',
    },
    'kr': {
        'frequency_limit': '7일 이내 총 빈도수가 한계치({})를 초과했습니다. 타겟 중복 노출이 많으니, 타겟을 확장하거나 광고 일시 중지 후 일주일 뒤에 다시 재개하는 것이 좋습니다.'.format(CONDITIONS['frequency_limit']),
        'spend_boom': "광고비 지출 금액이 전일 대비 {}배 이상 상승했습니다. 주의가 필요합니다.".format(CONDITIONS['spend_times_for_boom']),
        'spend_down': "광고비 지출 속도가 상당히 줄어들었습니다. 타겟 크기를 확대하거나, 광고 종료 날짜를 앞당기는 것이 좋습니다.",
        'spend_up': "광고비 지출 속도가 상당히 증가했습니다. 타겟 크기를 축소하거나, 광고 종료 날짜를 늘리는 것이 좋습니다.",
        'spend_unstable': "광고비 지출이 불안정합니다. 타겟 사이즈나 광고 기간을 확인해보시기 바랍니다.",
        'cpm_avg_limit': "특정일의 CPM이 과도하게 증가했습니다. 광고 최적화 목표 혹은 타겟 설정을 변경하는 것이 좋습니다.",
        'cpm_limit': "CPM이 한계치를 초과했습니다. 광고 최적화 목표 혹은 타겟 설정을 변경하는 것이 좋습니다.",
        'no_link_click': "일 동안 링크 클릭이 없습니다. 광고 설정을 확인 후 변경하는 것이 좋습니다.",
        'cpc_limit': "CPC(링크클릭)가 한계치를 초과했습니다. 광고 설정을 확인 후 변경하는 것이 좋습니다.",
        'ctr_bad': "광고에 대한 반응도(전체 클릭률)가 낮습니다. 광고 콘텐츠(이미지, 동영상, 광고 카피)를 개선하거나, 좀 더 적합한 타겟으로 변경하는 것이 좋습니다.",
        'bound_clicks_ctr_bad_with_canvas': "광고 타겟의 외부링크 유입율이 낮습니다. 성별 및 연령 등 타겟을 더 세분화하세요.",
        'bound_clicks_ctr_bad_no_canvas': "광고 반응이 외부링크로 연결되지 못하고 있습니다. 캔버스(Canvas) 제작 등 고객을 외부링크로 유도하세요.",
        'relevance_score': '관련성 점수가 너무 낮습니다. 광고 콘텐츠(이미지, 동영상, 광고 카피 등)를 개선해야합니다.',
    },
}