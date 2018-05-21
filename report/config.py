DATABASE = {
    "diana": {
        "uri": "mongodb://wizpace:wizpace0@mongo.diana.business:27017/diana",
        "name": "diana"
    },
    "autobidding": {
        "uri": "mongodb://autobidding:autobid0@bid.diana.business:27017/autobidding",
        "name": "autobidding"
    }
}

MAIL = {
    "login_id": "support@wizpace.com",
    "login_pw": "wizpace0",
    "from": "support@wizpace.com",
    "recipients": [
        # "support@wizpace.com",
        "tony.hwang@wizpace.com",
    ]
}

FETCH = {
    "from_days": 1,
    "min_imp_limit": 10
}

MAIL_FORM = {
    "items": [
        "spend",
        "impressions",
        "cpm",
        "reach",
        "frequency",
        "total_actions",
        "cost_per_total_action",
        "cost_per_inline_post_engagement",
        "clicks",
        "ctr",
        "cpc",
        "unique_clicks",
        "cost_per_unique_click",
        "inline_link_clicks",
        "inline_link_click_ctr",
        "cost_per_inline_link_click",
        "outbound_clicks",
        "outbound_clicks_ctr",
    ],
    "translate": {
        "recommendation": {
            "en": "Recommendation",
            "kr": "추천 사항",
        },
        "feature": {
            "en": "Feature",
            "kr": "지표",
        },
        "value": {
            "en": "Value",
            "kr": "값",
        },
        "spend": {
            "en": "Spend",
            "kr": "지출",
        },
        "impressions": {
            "en": "Impressions",
            "kr": "노출",
        },
        "cpm": {
            "en": "CPM",
            "kr": "CPM",
        },
        "reach": {
            "en": "Reach",
            "kr": "도달",
        },
        "frequency": {
            "en": "Frequency",
            "kr": "빈도",
        },
        "total_actions": {
            "en": "Total Actions",
            "kr": "총 행동",
        },
        "cost_per_total_action": {
            "en": "CPA(Actions)",
            "kr": "행동 당 비용",
        },
        "cost_per_inline_post_engagement": {
            "en": "CPA(Post Engagement)",
            "kr": "포스트 참여 당 비용",
        },
        "clicks": {
            "en": "Clicks",
            "kr": "클릭",
        },
        "ctr": {
            "en": "CTR",
            "kr": "클릭률",
        },
        "cpc": {
            "en": "CPC",
            "kr": "CPC",
        },
        "unique_clicks": {
            "en": "Clicks(Unique)",
            "kr": "클릭(고유)",
        },
        "cost_per_unique_click": {
            "en": "CPC(Unique)",
            "kr": "CPC(고유)",
        },
        "inline_link_clicks": {
            "en": "Clicks(Inline)",
            "kr": "클릭(내부링크)",
        },
        "inline_link_click_ctr": {
            "en": "CTR(Inline)",
            "kr": "CTR(내부링크)",
        },
        "cost_per_inline_link_click": {
            "en": "CPC(Inline)",
            "kr": "CPC(내부링크)",
        },
        "outbound_clicks": {
            "en": "Clicks(Outbound)",
            "kr": "클릭(외부)",
        },
        "outbound_clicks_ctr": {
            "en": "CTR(Outbound)",
            "kr": "CTR(외부)",
        },
        "footer_message": {
            "en": "You can analyze periodic and detailed data on Diana",
            "kr": "기간별 광고 데이터 및 자세한 분석은 아래 홈페이지에서 확인 가능합니다",
        },
    },
}
