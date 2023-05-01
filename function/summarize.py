import asyncio
import functools
import json
import time
from typing import Optional, Tuple

import requests

prompt = {
    "summarize": "summarize the article above and preserve information on \
                                                           the following concepts: Personnel/Human Resources, Time and Place, Object/Thing. ",
    "finalize": """
            Please help me gather data from various media sources above and analyze it across multiple articles to recognize similarities and differences. 
            For instance, if several articles report on the launch of a new Tesla car, one source might state the retail price as $10, while another mentions it as $15. 
            The similarities between the articles would be that they all cover the new car launch, while the differences would be the varying retail prices reported. 
            The final output should include a summary paragraph followed by a list of similarities and differences, 
            where the differences are presented in the format of source A reporting a price of $10, while source B reports a price of $15.
            response should be formed organized and neat in html layout, give me the h3 title and highlight the keyword as bold.
        """,
}


class SummaryAgent(object):
    def __init__(self, model_type="gpt-3.5-turbo", agent_type="chat", temperature=0.7):
        self.__check_apikey_endpoint = "https://api.openai.com/v1/models"
        self.__agent_role = {
            "role": "system",
            "content": "You are a very professional news artlce summization and analysis agent.",
        }
        self.model_type = model_type
        self.openai_payload = {
            "model": self.model_type,
            "messages": "",
            "temperature": temperature,
        }

        if agent_type == "chat":
            self.openai_chat_endpoint = "https://api.openai.com/v1/chat/completions"

    def is_valid_api_key(self, apikey: str = "") -> Tuple[bool, Optional[dict]]:
        # Set the headers for the API request
        tmp = {"Content-Type": "application/json", "Authorization": f"Bearer {apikey}"}
        # Send the API request
        response = requests.get(self.__check_apikey_endpoint, headers=tmp)

        is_valid_code = response.status_code == 200

        if is_valid_code:
            header = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {apikey}",
            }
        else:
            header = None
        return is_valid_code, header

    def ask(
        self,
        message: str = "",
        customize_prompt: str = "",
        state: str = "summarize",
        api_key: str = "",
    ) -> str:
        start = time.time()
        is_valid, header = self.is_valid_api_key(api_key)
        if not is_valid:
            return "[error]: openai api-key is invalid"

        if state == "customize":
            message += " " + customize_prompt
        elif state == "summarize":
            message += " " + prompt["summarize"]
        elif state == "finalize":
            message += " " + prompt["finalize"]
        else:
            assert state in [
                "summarize",
                "finalize",
                "customize",
            ], "state only support summarize, finalize and customize"

        messages = [
            self.__agent_role,
            {"role": "user", "content": message},
        ]

        self.openai_payload.update({"messages": messages})

        response = requests.post(
            url=self.openai_chat_endpoint,
            headers=header,
            data=json.dumps(self.openai_payload),
        )

        response_json = response.json()
        # print(response_json)
        end = time.time()
        print(f"Ask Time: {end-start}")
        if "error" in response_json:
            return (
                f'[error]: openai api call error: [{response_json["error"]["type"]}]'
                + response_json["error"]["message"]
            )
        return response_json["choices"][0]["message"]["content"]
