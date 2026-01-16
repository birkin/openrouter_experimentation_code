## from <https://openrouter.ai/docs/quickstart#using-the-openrouter-api-directly>

import datetime
import json
import os
from typing import Any

import httpx

## load the API key from the .env file
from dotenv import load_dotenv


def load_config() -> tuple[str, str, str]:
    """
    Loads the OpenRouter API key, model, and prompt file from the environment.
    Called by main().
    """
    load_dotenv()
    openrouter_api_key: str = os.environ['OPENROUTER_API_KEY']
    openrouter_model: str = os.environ['OPENROUTER_MODEL']
    openrouter_prompt_file: str = os.environ['OPENROUTER_PROMPT_FILE']
    return openrouter_api_key, openrouter_model, openrouter_prompt_file


def load_prompt(prompt_file: str) -> str:
    """
    Loads the prompt from the file.
    Called by main().
    """
    with open(prompt_file, 'r') as f:
        prompt: str = f.read()
    return prompt


def call_openrouter(api_key: str, model: str, prompt: str) -> dict[str, Any]:
    """
    Calls the OpenRouter API.
    Called by main().
    """
    response: httpx.Response = httpx.post(
        url='https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {api_key}',
            # 'HTTP-Referer': '<YOUR_SITE_URL>',  # Optional. Site URL for rankings on openrouter.ai.
            # 'X-Title': '<YOUR_SITE_NAME>',  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps(
            {
                'model': model,  # Optional
                'transforms': ['middle-out'],
                'messages': [{'role': 'user', 'content': prompt}],
            }
        ),
    )

    jsn: dict[str, Any] = response.json()
    return jsn


def main() -> None:
    """
    Main controller function.
    """
    openrouter_api_key, openrouter_model, openrouter_prompt_file = load_config()
    prompt: str = load_prompt(openrouter_prompt_file)

    start_time: datetime.datetime = datetime.datetime.now()
    jsn: dict[str, Any] = call_openrouter(openrouter_api_key, openrouter_model, prompt)

    ## output -----------------------------------------------------------
    print(json.dumps(jsn, indent=2))
    print('\n\n')

    time_taken: datetime.timedelta = datetime.datetime.now() - start_time
    print(f'time taken, ``{time_taken}``')


if __name__ == '__main__':
    main()
