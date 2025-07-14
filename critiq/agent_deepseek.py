import json
import os
import requests
import random
import time
from typing import Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

RATE_LIMIT_RETRY_DELAY = 60
WORKFLOW_AGENT_LOGFILE = os.getenv("WORKFLOW_AGENT_LOGFILE", None)
from tqdm import tqdm

class Agent:
    def __init__(
        self,
        system: str | None = None,
        base_url: str | None = None,
        api_keys: str | list[str] | None = None,
        request_kwargs: dict[str, Any] = None,
    ):
        self.system = system
        if self.system is None:
            self.history = []
        else:
            self.history = [{"role": "system", "content": self.system}]
        self.base_url = base_url
        self.api_keys = api_keys if api_keys else os.getenv("OPENAI_API_KEY", "EMPTY")
        self.headers_list = [{'Authorization': key, 'Content-Type': 'application/json'} for key in self.api_keys ]
        self.request_kwargs = request_kwargs or {}

    # deepseek 
    # def chatDeepseek(self, system_info, user_info, headers):
    #     ds_prompt = {
    #         "inputs": {"system": system_info, "user": user_info},
    #         "user": "abc-123"
    #     }
    #     response = requests.post(url=self.base_url, headers=headers, data=json.dumps(ds_prompt))
        
    #     try:
    #         response = json.loads(response.text)
    #         # pdb.set_trace()
    #         response = response["data"]['outputs']['text'] 


    #         # pdb.set_trace()
    #     except Exception as e:
    #         print("Deepseek API call error: ", e)
    #         print(headers)
    #         print(response)
    #         response = ""
    #     return response


    # doubao qwen
    def chatDeepseek(self, system_info, user_info, headers):
        doubao_prompt = {
        "inputs": {"system_info": system_info, "user_info": user_info},
        "user": "abc-123"
        }

        url = 'https://mify-be.pt.xiaomi.com/api/v1/workflows/run'
        max_try_time = 200  # 最大重试次数
        try_time = 0       # 当前重试次数
        base_delay = 1     # 初始等待时间

        while try_time < max_try_time:
            try:
                # 发送POST请求
                response = requests.post(url=url, headers=headers, data=json.dumps(doubao_prompt))
                # print(response)
                if response.status_code == 200:  # 请求成功
                    response_data = json.loads(response.text)
                    # print(response_data)
                    outputs = response_data["data"]['outputs']['outputs']
                    return outputs
                
                elif response.status_code == 429:  # 速率限制错误
                    delay = base_delay * (2 ** try_time)  # 指数退避策略
                    print(f"API请求速率限制，状态码：429，等待{delay}秒后重试...")
                    time.sleep(delay)
                
                else:  # 其他错误
                    print(f"API请求失败，状态码：{response.status_code}，响应内容：{response.text}")
                    return False, ''
            
            except Exception as err:
                print("发生异常data error:",err)
                print(f"响应内容：{response.text}")
            
            finally:
                try_time += 1
        
        return False, ""



    def chat_completion(self, messages: List[dict], stream: bool = True) -> str:
        system_info = ""
        user_info = ""
        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role == "system":
                system_info = content
            elif role == "user":
                user_info = content
        
        # 使用随机选择的 API key

        headers = random.choice(self.headers_list)

        response = self.chatDeepseek(system_info, user_info, headers)
        return response

    def __call__(self, prompt: str, stream: bool = True) -> str | None:
        self.history.append({"role": "user", "content": prompt})
        try:
            response = self.chat_completion(self.history, stream=stream)
            if not response:
                raise ValueError("Empty response from API")
        except Exception as e:
            self.history.pop()
            print(e)
            return None
        self.history.append({"role": "assistant", "content": response})
        if WORKFLOW_AGENT_LOGFILE:
            with open(WORKFLOW_AGENT_LOGFILE, "a") as f:
                f.write(
                    json.dumps(
                        {
                            "time": time.time(),
                            "prompt": prompt,
                            "response": response,
                            "history": self.history,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        #print(response)
        return response

    def get_last_reply(self):
        if self.history and self.history[-1]["role"] == "assistant":
            return self.history[-1]["content"]
        return None

    def forget_last_turn(self):
        while self.history and self.history[-1]["role"] != "user":
            self.history.pop()
        if self.history and self.history[-1]["role"] == "user":
            self.history.pop()

    def fork(self) -> "Agent":
        forked = Agent(
            system=self.system, 
            api_keys=self.api_keys, 
            base_url=self.base_url,
            request_kwargs=self.request_kwargs,
        )
        forked.history = self.history[:]
        return forked