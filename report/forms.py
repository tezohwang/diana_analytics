from .config import MAIL_FORM

import datetime


def create_mail_facebook(content):
    '''
    '''
    if not content['facebook']['ads']:
        return False

    lang = content['lang']

    form = ''
    # html 시작
    form += '<html>'
    # head 파트
    form += '''
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
            td, th {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-collapse: collapse;
                text-align: center;
                padding: 5px;
            }
            tr:nth-child(even) {background-color: #f1fbf2;}
            @media(max-width: 600px) {

                table {
                    width: 90%;
                    max-width: 580px;
                }

                h1 {
                    font-size: 40px;
                    line-height: 40px;
                }

                p {
                    font-size: 18px;
                }

                td {
                    font-size: 10px;
                    line-height: 20px;
                }
            }
        </style>
    </head>
    '''
    # body 파트 상단
    form += '''
    <body>
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;text-indent:0px;text-transform:none;font-size:20px;white-space:normal;word-spacing:0px;width:759px">
                <tr>
                    <td style="background-color:#52A4FC;color:#000000;padding:20px;">
                        <img alt="logo"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/diana_logo_white.png"
                            width="120" style="display: block;"/>
                    </td>
                </tr>
                <tr>
                    <td style="background-color:#FFFFFF;color:#333333;padding:0px; text-align: center;position: relative; border-color: #FFFFFF">
                        <h1 style="padding-top: 60px">{} <br> Diana Report</h1>
                        <hr width="20%" color="#00c73c">
                        <p style="padding-top: 20px"><b>User: {}</b></p>
                        <img alt="graph Image"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/header_image2.png"
                            width="100%" height="auto"/>
                    </td>
                </tr>
            </table>
            <br>
        </div>
        <div>
            <img alt="facebook_logo" src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/facebook_logo.png" width="120" style="display: block;padding: 5px;"/>
        </div>
    '''.format((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), content['username'])

    ads = content['facebook']['ads']
    for ad in ads:
        # body > content 시작
        form += '''
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
        '''
        # body > content > '캠페인 영역 라인 표시'
        form += '''
        <tr>
            <th colspan="10"
                style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                {}
            </th>
        </tr>
        <tr style="color:#00c73c;">
        '''.format(ad['name'])
        form += '''
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
        '''.format(MAIL_FORM['translate']['feature'][lang], MAIL_FORM['translate']['value'][lang])

        currency = ad['currency']
        items = MAIL_FORM['items']
        
        for item in items:
            if item in ad['yesterday']:
                form += '<tr>'
                form += '<td>{}</td>'.format(MAIL_FORM['translate'][item][lang])
                item_value = format(round(ad['yesterday'][item], 2), ',')
                if item in ['spend', 'cost_per_total_action', 'cost_per_inline_post_engagement', 'cpc', 'cost_per_unique_click', 'cost_per_inline_link_click']:
                    item_value += ' {}'.format(currency)
                form += '<td>{}</td>'.format(item_value)
                form += '</tr>'

        form += '</table>'

        # 추천 사항이 있으면 작성
        if ad['recos']:
            form += '''
                <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
                <tr>
                    <th colspan="10"
                        style="border:1px solid #A8D2FF;border-collapse:collapse;background-color:#A8D2FF;color: #FFFFFF;padding: 5px;font-size: 13px">
                        {}
                    </th>
                </tr>
            '''.format(MAIL_FORM['translate']['recommendation'][lang])
            for reco in ad['recos']:
                # tr
                form += '<tr>'
                # reco 데이터
                form += '<td>{}</td>'.format(reco)
                form += '</tr>'
            form += '</table>'

    form += '''
        <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
            <tr>
                <td>
                <br>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;">{}</p>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;"><a href="http://www.diana.business">www.diana.business</a></p>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;">2017 @ COPYRIGHT - DIANA</p>
                <img alt="diana logo img" src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/diana_logo_gray.png" width="104px" height="auto" style="padding: 10px" />
                </td>
            </tr>
        </table>
    </body>
    </html>
    '''.format(MAIL_FORM['translate']['footer_message'][lang])
    return form

def create_mail_naver(content):
    '''
    '''
    if not content['naver']['campaigns']:
        return False
    form = ''
    # html 시작
    form += '<html>'
    # head 파트
    form += '''
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
            td, th {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-collapse: collapse;
                text-align: center;
                padding: 5px;
            }
            tr:nth-child(even) {background-color: #f1fbf2;}
            @media(max-width: 600px) {

                table {
                    width: 90%;
                    max-width: 580px;
                }

                h1 {
                    font-size: 40px;
                    line-height: 40px;
                }

                p {
                    font-size: 18px;
                }

                td {
                    font-size: 10px;
                    line-height: 20px;
                }
            }
        </style>
    </head>
    '''
    # body 파트 상단
    form += '''
    <body>
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;text-indent:0px;text-transform:none;font-size:20px;white-space:normal;word-spacing:0px;width:759px">
                <tr>
                    <td style="background-color:#52A4FC;color:#000000;padding:20px;">
                        <img alt="logo"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/diana_logo_white.png"
                            width="120" style="display: block;"/>
                    </td>
                </tr>
                <tr>
                    <td style="background-color:#FFFFFF;color:#333333;padding:0px; text-align: center;position: relative; border-color: #FFFFFF">
                        <h1 style="padding-top: 60px">{} <br> Diana Report</h1>
                        <hr width="20%" color="#00c73c">
                        <p style="padding-top: 20px"><b>User: {}</b></p>
                        <img alt="graph Image"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/header_image2.png"
                            width="100%" height="auto"/>
                    </td>
                </tr>
            </table>
            <br>
        </div>
        <div>
            <img alt="naver_logo" src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/naver_logo.png" width="120" style="display: block;padding: 5px;"/>
        </div>
    '''.format((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), content['username'])

    if content['naver']['campaigns']:
        # body > content 시작
        form += '''
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
        '''
        # body > content > '캠페인 영역 라인 표시'
        form += '''
        <tr>
            <th colspan="10"
                style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                캠페인
            </th>
        </tr>
        <tr style="color:#00c73c;">
        '''
        form += '''
        <tr>
            <th>캠페인</th>
            <th>비용</th>
            <th>노출</th>
            <th>클릭</th>
            <th>클릭률</th>
            <th>CPC</th>
            <th>전환</th>
        </tr>
        '''
        for campaign in content['naver']['campaigns']:
            # tr
            form += '<tr>'
            # 계정 아이디
            # form += '<td>{}</td>'.format(campaign['network_id'])
            # 캠페인 이름 & 아이디
            form += '<td>{}</td>'.format(campaign['name'])
            # form += '<td>{}</td>'.format(campaign['campaign_id'])
            # 인사이트 데이터
            form += '<td>{}</td>'.format(
                    format(int(campaign['yesterday']['spend']), ','))
            form += '<td>{}</td>'.format(
                    format(int(campaign['yesterday']['impressions']), ','))
            form += '<td>{}</td>'.format(
                    format(int(campaign['yesterday']['clicks']), ','))
            form += '<td>{}</td>'.format(
                    round(campaign['yesterday']['ctr'], 2))
            form += '<td>{}</td>'.format(
                    format(int(campaign['yesterday']['cpc']), ','))
            # 전환은 있을 경우에만
            try:
                form += '<td>{}</td>'.format(
                        format(int(campaign['yesterday']['ccnt']), ','))
            except Exception as e:
                form += '<td>{}</td>'.format(0)
            # form += '<td>{}</td>'.format(campaign['dateStart'])
            # /tr
            form += '</tr>'
        form += '</table>'

        # 애드그룹이 있으면 작성
        if content['naver']['adgroups']:
            form += '''
                <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
                <tr>
                    <th colspan="10"
                        style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                        광고그룹
                    </th>
                </tr>
                <tr>
                    <th>광고그룹</th>
                    <th>비용</th>
                    <th>노출</th>
                    <th>클릭</th>
                    <th>클릭률</th>
                    <th>CPC</th>
                    <th>전환</th>
                </tr>
            '''
            for adgroup in content['naver']['adgroups']:
                # tr
                form += '<tr>'
                # 계정 아이디
                # form += '<td>{}</td>'.format(adgroup['network_id'])
                # 광고그룹 이름 & 아이디
                form += '<td>{}</td>'.format(adgroup['name'])
                # form += '<td>{}</td>'.format(adgroup['adgroup_id'])
                # 인사이트 데이터
                form += '<td>{}</td>'.format(
                        format(int(adgroup['yesterday']['spend']), ','))
                form += '<td>{}</td>'.format(
                        format(int(adgroup['yesterday']['impressions']), ','))
                form += '<td>{}</td>'.format(
                        format(int(adgroup['yesterday']['clicks']), ','))
                form += '<td>{}</td>'.format(
                        round(adgroup['yesterday']['ctr'], 2))
                form += '<td>{}</td>'.format(
                        format(int(adgroup['yesterday']['cpc']), ','))
                # 전환은 있을 경우에만
                try:
                    form += '<td>{}</td>'.format(
                            format(int(adgroup['yesterday']['ccnt']), ','))
                except Exception as e:
                    form += '<td>{}</td>'.format(0)
                # form += '<td>{}</td>'.format(adgroup['dateStart'])
                # /tr
                form += '</tr>'
        form += '</table>'

        # 키워드 이슈가 있으면 작성
        if content['naver']['recos']:
            form += '''
                <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
                <tr>
                    <th colspan="10"
                        style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                        키워드
                    </th>
                </tr>
                <tr>
                    <th>키워드명</th>
                    <th>주요 이슈</th>
                </tr>
            '''
            for reco in content['naver']['recos']:
                # tr
                form += '<tr>'
                # 키워드 이름
                form += '<td>{}</td>'.format(reco['name'])
                # 이슈 데이터
                form += '<td>{}</td>'.format(reco['reco'])
                form += '</tr>'
        form += '</table>'
    form += '''
        <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
            <tr>
                <td>
                <br>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;">기간별 광고 데이터 및 자세한 분석은 아래 홈페이지에서 확인 가능합니다</p>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;"><a href="http://www.diana.business">www.diana.business</a></p>
                <p style="font-size:15px;line-height:20px;font-family: 'AppleSDGothicNeo-Light', Helvetica, Arial, serif; text-align:center;">2017 @ COPYRIGHT - DIANA</p>
                <img alt="diana logo img" src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/diana_logo_gray.png" width="104px" height="auto" style="padding: 10px" />
                </td>
            </tr>
        </table>
    </body>
    </html>
    '''
    return form
