import requests
import re
import os
import openai
import random
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()


class Slack_bot:
    def __init__(self, icon=[':piggy:', ':gorilla:', ':dog:']):
        self.icon = icon
        self.idx = random.choice([i for i in range(len(self.icon))])
        self.web_hook = os.environ['WEB_HOOK_URL']

    def __call__(self, msg='Messgaes'):
        WEB_HOOK_URL = self.web_hook

        requests.post(WEB_HOOK_URL, data=json.dumps({
            "text": msg,
            "icon_emoji": self.icon[self.idx],
            "username": self.icon[self.idx][1:-1],
        }))


def get_urls(url):
    # HTTP GETリクエストを送信
    response = requests.get(URL)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        # レスポンスのHTMLをパース
        soup = BeautifulSoup(response.text, "html.parser")

        # パースしたHTMLから特定の要素を取得する例
        links = soup.find_all("a")  # <a>タグのリンクを全て取得

        url_list = list()
        for link in links:
            url = link.get("href")
            if re.match('https://techcrunch.com/\d', url):
                url_list.append(url)

        return sorted(set(url_list), key=url_list.index)
    else:
        return list()


def get_summary(url_list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは記事を要約する便利なアシスタントです"},
            {"role": "user", "content": "これから送るURLの内容について，タイトル・URL・内容の要約をそれぞれ記載してください"},
            {"role": "assistant",
                "content": "もちろんです。お送りいただくURLの内容に基づいて、タイトル、URL、および内容の要約を提供しますので、URLをお教えください。"},
            {"role": "user", "content": url_list},
        ],
    )
    return response["choices"][0]["message"]["content"].strip()


if __name__ == '__main__':

    URL = "https://techcrunch.com/"
    url_list = get_urls(URL)

    if not len(url_list):
        print('List is empty.')
        exit()

    # APIキーの設定
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # 1分間にリクエストは3回まで
    slice_idx = 4
    if slice_idx >= len(url_list):
        slice_idx = len(url_list) - 1
    url_list = url_list[:slice_idx]

    slack_bot = Slack_bot()
    for i in range(len(url_list)):
        sumarry = get_summary(url_list[i])
        slack_bot(msg=sumarry)
