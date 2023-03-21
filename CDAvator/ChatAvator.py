import httpx
from pprint import pprint 
from httpx_socks import SyncProxyTransport, AsyncProxyTransport

import time
from typing import Optional
from collections import defaultdict
# from os import environ, getenv

openai_key = "sk-<YOUR_KEY>"
openai_chat_api = "https://api.openai.com/v1/chat/completions"
proxy = 'socks5://127.0.0.1:1087'
# proxy = 'socks5://100.64.0.15:11081'
# proxy = 'socks5://100.64.0.42:7890'


headers = {
    "Authorization": f"Bearer {openai_key}"
}

histories = defaultdict(list)


def get_reply(messages):
    transport = SyncProxyTransport.from_url(proxy)
    try:
        with httpx.Client(transport=transport) as client:
            resp = client.post(
                openai_chat_api, json={
                    "model": "gpt-3.5-turbo", "messages": messages}, 
                    headers=headers,
                timeout=5 * 60)
            data = resp.json()
            if data.get('choices'):
                reply = data['choices'][0]['message']
                return reply['content']
    except Exception as e:
        import logging
        logging.exception(e)
        return "请求失败，请重试"


def test():
    text = """
    中国上海对外贸易中心就上述事项于1994年4月22日向对外经贸部作出请示【（94）中沪贸协办字第035号】，对外经贸部于1994年6月24日做出了《关于中国上海对外贸易中心调整股东投资方案的批复》【1004外经贸政促函字第1016号】同意上述股东调整方案。
    """

    result = get_reply([
    {"role": "user", 
    "content": "You are a helpful assistant that extract all named-entities in Chinese texts."
                "In addition, we treat datetime, government files (i.e., 淮财办专函【2019】08号，杭政办函[2020]7号) and products (i.e., 铁质管道，手工艺品) are also entities."},
    {"role": "system", 
    "content": "OK, I will list all entities and their character-level indexes in the text, with their entity types. Now, please give me a source text."},
    {"role": "user", 
    "content": # f"I will give you a source text, after extracting entities from it, list all entities at first."
                # f"Then in the source text, replace every character of extracted entities with token *"
                f"生成一个表格，第一列是实体，第二列是类型，第三列是起止位置。要求仅生成表格，不要生成解释文本。"
                f"Here is the source Chinese text: {text}."}
    ])

    print(result)


if __name__ == "__main__":
    pass