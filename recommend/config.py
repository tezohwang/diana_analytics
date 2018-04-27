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

THRESHOLD = {
    "spend": {
        "bestgo": 500000,
        "baronmotors": 500000,
        "uiseong": 3000,
        "wizpace": 1500,
    },
    'no_ccnt_spend': {
        "bestgo": 50000,
        "baronmotors": 50000,
        "uiseong": 1000,
        "wizpace": 500,
    },
    'avg_cpc_times': {
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
    },
    'avg_cpm_times': {
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
    },
    'avg_imp_times': {
        "bestgo": 2.0,
        "baronmotors": 2.0,
        "uiseong": 2.0,
        "wizpace": 5.0,
    },
}
