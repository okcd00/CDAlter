import json
import httpx
from pprint import pprint


DUMMY_CONTENTS = {
    "jsonrpc": "2.0",
    "method": "LMT_handle_jobs",
    "params": {
        "jobs": [
            {
                "kind": "default",
                "sentences": [
                    {
                        "text": "<CHANGE_HERE>",
                        "id": 0,
                        "prefix": ""
                    }
                ],
                "raw_en_context_before": [],
                "raw_en_context_after": [],
                "preferred_num_beams": 4,
                "quality": "fast"
            }
        ],
        "lang": {
            "preference": {
                "weight": {
                    "DE": 0.01166,
                    "EN": 30.85918,
                    "ES": 0.01381,
                    "FR": 0.01995,
                    "IT": 0.01527,
                    "JA": 0.0673,
                    "NL": 0.00997,
                    "PL": 0.01002,
                    "PT": 0.01155,
                    "RU": 0.00817,
                    "ZH": 1.79458,
                    "BG": 0.00607,
                    "CS": 0.00756,
                    "DA": 0.00857,
                    "EL": 0.00571,
                    "ET": 0.0065,
                    "FI": 0.00767,
                    "HU": 0.00711,
                    "LT": 0.00857,
                    "LV": 0.00493,
                    "RO": 0.01064,
                    "SK": 0.00842,
                    "SL": 0.00641,
                    "SV": 0.00896,
                    "ID": 0.00881,
                    "TR": 0.00679,
                    "UK": 0.00698,
                    "NB": 0.00938,
                    "KO": 0.01236
                },
                "default": "default"
            },
            "source_lang_user_selected": "auto",
            "target_lang": "ZH"
        },
        "priority": -1,
        "commonJobParams": {
            "mode": "translate",
            "browserType": 1
        },
        "timestamp": 1679367167886  # int(time.time() * 100)
    },
    "id": 76910164
}


class Translator(object):
    def __init__(self):
        self.proxies = 'socks5://100.64.0.15:11081'
        self.url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'

        from httpx_socks import SyncProxyTransport, AsyncProxyTransport
        self.transport = SyncProxyTransport.from_url(self.proxies)

    def construct_contents(self, text):
        dc = DUMMY_CONTENTS
        dc['params']['jobs'][0]['sentences'][0]['text'] = text
        try:
            with httpx.Client(transport=self.transport) as client:
                resp = client.post(self.url, json=dc, timeout=5 * 60)                
                return resp.json()
        except Exception as e:
            import logging
            logging.exception(e)
            return "请求失败，请重试"

    def __call__(self, text):
        json_str = self.construct_contents(text)
        print(json_str)


if __name__ == "__main__":
    import time
    print(int(time.time() * 100))
