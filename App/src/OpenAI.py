import os

from openai import AsyncOpenAI
from App.src.Schemas.UserData import PrayResponseRequest

secret_key = os.environ.get("DEEPSEEK_SECRET_KEY")
pray_prompt = os.environ.get("DEEPSEEK_PRAY_PROMPT")

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
