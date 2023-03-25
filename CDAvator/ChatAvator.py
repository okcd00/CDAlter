import httpx
from pprint import pprint 
from httpx_socks import SyncProxyTransport, AsyncProxyTransport

import time
from typing import Optional
from collections import defaultdict
from os import environ, getenv

openai_chat_api = "https://api.openai.com/v1/chat/completions"
openai_key = environ['OPENAI_KEY'] # can be found in chatgpt/ai/api_test.ipynb
proxy = getenv('OPENAI_PROXY')
# proxy = 'socks5://100.64.0.15:11081'
# proxy = 'socks5://100.64.0.42:7890'


headers = {
    "Authorization": f"Bearer {openai_key}"
}

histories = defaultdict(list)


def get_reply(prompt, history=None):
    transport = SyncProxyTransport.from_url(proxy)
    try:
        if history is None:
            history = []
        history.append({"role": "user", "content": prompt})
        with httpx.Client(transport=transport) as client:
            resp = client.post(
                openai_chat_api, 
                json={"model": "gpt-3.5-turbo", "messages": history}, 
                headers=headers, timeout=5 * 60)
            data = resp.json()
            if data.get('choices'):
                reply = data['choices'][0]['message']
                history.append(reply)
                return reply['content']
            else:
                raise Exception("No Response. \n{}".format(data))
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


def input_with_enter(hint=''):
    """遇到一个空行返回结果"""
    text = []
    pre_t = input(hint)
    while pre_t != '':
        text.append(pre_t)
        pre_t = input()
    print('<Jarvis: received>')
    return '\n'.join(text)


def save_history(history, save_path):
    """json line"""
    import json
    import time 
    with open(save_path, 'a') as f:
        f.write(time.strftime('%Y/%m/%d-%H:%M:%S '))
        json.dump(history, f)
        f.write('\n')


def save_and_clear_history(history, instruct='', save_path='./logs/chat_history.log'):
    save_history(history, save_path)
    history = [{"role": "system", "content": instruct}]
    print("已经清除历史记录，请重新提问。")
    return history


def start_chat(instruct, multiline_input=True):
    history = [{"role": "system", "content": instruct}]
    try:
        while True:
            print('-'*40+'\n')
            if multiline_input:
                question = input_with_enter("问：")
            else:
                question = input('问：')
            if question == 'clear':
                history = save_and_clear_history(history, instruct)
                continue
            rep = get_reply(question, history)
            print("\nJarvis:\n", rep)
    except Exception as e:
        save_and_clear_history(history)
        raise e 


def main():
    import sys
    instruct = "你是一个叫作Jarvis的专业工作助手，需要回答各种具备专业知识的问题，要求回答严谨、精确。"
    if len(sys.argv) > 1:
        instruct = sys.argv[1]
    start_chat(instruct=instruct)


if __name__ == "__main__":
    # pip install -r requirements.txt
    """
    export OPENAI_PROXY=127.0.0.1:1081
    OPENAI_KEY=sk-<YOUR_KEY> python start_chat.py "You are my friend and you know my name is Kari."
    """
    main()
