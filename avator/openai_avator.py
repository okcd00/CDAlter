# coding: utf-8
# ==========================================================================
#   Copyright (C) since 2024 All rights reserved.
#
#   filename : openai_avator.py
#   author   : chendian / okcd00@qq.com
#   date     : 2024/07/15 00:17:48
#   desc     : 
#              
# ==========================================================================
import os, sys, time
import openai
import tiktoken
from pprint import pprint
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from memory.my_custom_access import OPENAI_API_KEY
from httpx_socks import SyncProxyTransport, AsyncProxyTransport


# 设置 HTTP 和 HTTPS 代理
os.environ['http_proxy'] = 'http://127.0.0.1:1081'
os.environ['https_proxy'] = 'http://127.0.0.1:1081'

class OpenAIAvator(object):
    def __init__(self) -> None:
        openai.api_key = OPENAI_API_KEY

        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.session = requests.Session()
        self.session.proxies = {
            "http": "http://127.0.0.1:1081", 
            "https": "https://127.0.0.1:1081"}

        self.retry = Retry(total=5, backoff_factor=1, status_forcelist=[429,500,502,503,504])
        self.adaptor = HTTPAdapter(max_retries=self.retry)
        self.session.mount("http://", adapter=self.adaptor)
        self.session.mount("https://", adapter=self.adaptor)

    def count_token_counts(self, messages, model="gpt-3.5-turbo-0613"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")

    def count_token_counts_after(self, messages, model):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        token_count = response.usage.prompt_tokens
        print(f'{token_count} prompt tokens used.')
        return token_count

    def _query(self, model_name="gpt-3.5-turbo"):
        response = self.client.completions.create(
            model=model_name,
            prompt="Write a tagline for an ice cream shop."
        )
        return response

    def query(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )
        return response

    def query_json_mode(self):
        # Returns: "content": "{\"winner\": \"Los Angeles Dodgers\"}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": "Who won the world series in 2020?"}
            ]
        )
        return response
    

if __name__ == "__main__":
    avt = OpenAIAvator()
    ret = avt._query()
    pprint(ret)
