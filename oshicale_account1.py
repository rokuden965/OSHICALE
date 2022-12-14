# -*- coding: utf-8 -*-

import os
import datetime
import re
import googleapiclient.discovery
import google.auth
import tweepy
import csv

def main():
    load()
    pinned_tw()

    print("ツイートデータ")
    print(okyu)
    #pre_okyu(既存の給仕日データ)とokyu(ツイートから取得した給仕日データ)が違えば(更新があれば)カレンダー反映
    if pre_okyu == okyu:
        print("変化なし")
    else:
        print("固定ツイート変更あり")
        calender(okyu)
    time_now = datetime.datetime.now()
    print(time_now)

def load():
    global pre_okyu
    print('account1↓')
    #既存お給仕日データ存在確認
    path = './account1_data.csv'
    is_file = os.path.isfile(path)
    if is_file:
        #既存お給仕日データ読込み
        with open("account1_data.csv") as f:
            reader = csv.reader(f)
            for pre_okyu in reader:
                print("既存データ")
                print(pre_okyu)
    else:
        with open("./account1_data.csv", "w")  as f:
            f.write("")
            f.close()
        pre_okyu = []

def pinned_tw():
    API_KEY = '###'
    API_KEY_SECRET = '###'
    BEARER_TOKEN = '###'
    ACCESS_TOKEN = '###'
    ACCSESS_TOKEN_SECRET = '###'

    #リファレンスの内容に沿って入力（https://docs.tweepy.org/en/stable/client.html）
    client = tweepy.Client(bearer_token = BEARER_TOKEN, consumer_key = API_KEY, consumer_secret = API_KEY_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCSESS_TOKEN_SECRET)
    #ユーザー名を指定
    input_username = 'account1'

    #固定ツイートを取得
    pinned_tweet = client.get_user(username=input_username,expansions="pinned_tweet_id")
    #固定ツイートを文字列として扱う
    s = str(pinned_tweet)
    #給仕日として固定ツイートから右に「 ♡」のついた数字を取得し行列に格納
    m_list = re.findall('n\d日',s) + re.findall('n\d\d日',s)

    l = m_list
    #行列から「n」を除去
    l_replace = [s.replace('n','') for s in l]
    #行列から「日」を除去
    global okyu
    okyu = [s.replace('日','') for s in l_replace]
    #給仕日をCSVファイルに格納
    with open('account1_data.csv', 'wt', encoding='utf-8') as f:
        # ライター（書き込み者）を作成
        writer = csv.writer(f)
        # ライターでデータ（リスト）をファイルに出力
        writer.writerow(okyu)

def calender():
    # 編集スコープの設定(今回は読み書き両方OKの設定)
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # カレンダーIDの設定
    calendar_id = '####@group.calendar.google.com'
    # 認証ファイルを使用して認証用オブジェクトを作成
    gapi_creds = google.auth.load_credentials_from_file('credentials.json', SCOPES)[0]        
    # 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

    dt=datetime.datetime.now()
    #okyuの中に入ってる要素の数だけ予定追加を行う
    for day in okyu:

    # 追加する予定の日時を設定
        time_begin = str(dt.year)+"-"+str(dt.month)+"-"+day+"T18:00:00"
        time_end = str(dt.year)+"-"+str(dt.month)+"-"+day+"T23:00:00"
        #print(time_begin)
   
        event= {
            # 予定のタイトル
            'summary': 'account1お給仕',
            # 予定の開始時刻
            'start': {
                'dateTime': time_begin,
                'timeZone': 'Japan'
            },
            # 予定の終了時刻
            'end': {
                'dateTime': time_end,
                'timeZone': 'Japan'
            },
        }
        
        # 予定を追加する
        event = service.events().insert(calendarId = calendar_id, body = event).execute()
    print("予定追加完了")

if __name__ == '__main__':
    main()
