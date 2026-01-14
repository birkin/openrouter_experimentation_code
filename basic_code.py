## from <https://openrouter.ai/docs/quickstart#using-the-openrouter-api-directly>


import datetime
import json
import os
from typing import Any

import requests

## load the API key from the .env file
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY: str = os.environ['OPENROUTER_API_KEY']
OPENROUTER_MODEL: str = os.environ['OPENROUTER_MODEL']

start_time: datetime.datetime = datetime.datetime.now()
response: requests.Response = requests.post(
    url='https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        # 'HTTP-Referer': '<YOUR_SITE_URL>',  # Optional. Site URL for rankings on openrouter.ai.
        # 'X-Title': '<YOUR_SITE_NAME>',  # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps(
        {
            'model': OPENROUTER_MODEL,  # Optional
            'messages': [{'role': 'user', 'content': 'What is the meaning of life?'}],
        }
    ),
)

## output -----------------------------------------------------------

jsn: dict[str, Any] = response.json()
print(json.dumps(jsn, indent=2))

print('\n\n')

time_taken: datetime.timedelta = datetime.datetime.now() - start_time
print(f'time taken, ``{time_taken}``')
