from recommend.database import connect_db

import requests
import json
import datetime


def main():
    db = connect_db('diana')
    db_check = db['db_check']
    try:
        result = list(db_check.find())
        print(result)
        print("db_check done: {}".format(datetime.datetime.now()))
    except Exception as e:
        data = json.dumps({"DB Error": str(e)}).encode('utf-8')
        r = requests.post('http://127.0.0.1:8000/report/send_mail', data=data)
        print(r)
        print("DB Error send_mail done: {}".format(datetime.datetime.now()))


if __name__ == '__main__':
    main()
