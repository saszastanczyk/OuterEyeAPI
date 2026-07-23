import os

from openai import AsyncOpenAI
from App.src.Schemas.Requests import PrayResponseRequest
from src.Schemas.UserData import UserData

secret_key = os.environ.get("DEEPSEEK_SECRET_KEY")
pray_prompt = os.environ.get("DEEPSEEK_PRAY_PROMPT")
analysis_prompt = os.environ.get("DEEPSEEK_ANALYSIS_PROMPT")

client = AsyncOpenAI(
    api_key=secret_key,
    base_url="https://api.deepseek.com")

async def get_pray_response(request:PrayResponseRequest) -> str:
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": pray_prompt},
            {"role": "user", "content": request.model_dump_json()}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

async def get_analysis_response(data:UserData) -> str:
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": analysis_prompt},
            {"role": "user", "content": data.model_dump_json()}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content
