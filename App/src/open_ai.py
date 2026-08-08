import os

from openai import AsyncOpenAI
from App.src.Schemas.requests import PrayResponseRequest
from src.Schemas.user_data import UserData
from src.Schemas.response_data import AIResponse

secret_key = os.environ.get("DEEPSEEK_SECRET_KEY")

client = AsyncOpenAI(
    api_key=secret_key,
    base_url="https://api.deepseek.com")

async def get_pray_response(request:PrayResponseRequest) -> str:
    pray_prompt = os.environ.get("DEEPSEEK_PRAY_PROMPT")
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": pray_prompt},
            {"role": "user", "content": request.model_dump_json()}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

async def get_analysis_response(data:AIResponse) -> str:
    analysis_prompt = os.environ.get("DEEPSEEK_ANALYSIS_PROMPT")
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": analysis_prompt},
            {"role": "system", "content": "Schema of your response:" + str(AIResponse.model_json_schema())},
            {"role": "user", "content": data.model_dump_json()}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    for r in response.choices:
        print(r.message.content)
    return response.choices[0].message.content
