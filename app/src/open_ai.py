import os

from openai import AsyncOpenAI
from app.src.Schemas.requests import PrayResponseRequest
from app.src.Schemas.user_data import UserData
from app.src.Schemas.response_data import AIResponse

secret_key = os.environ.get("AI_SECRET_KEY")
pray_prompt = os.environ.get("AI_PRAY_PROMPT")
analysis_prompt = os.environ.get("AI_ANALYSIS_PROMPT")
pray_temperature = float(os.environ.get("AI_PRAY_TEMPERATURE",default="0.5"))
analysis_temperature = float(os.environ.get("AI_ANALYSIS_TEMPERATURE",default="0.3"))
ai_url = os.environ.get("AI_URL")


client = AsyncOpenAI(
    api_key=secret_key,
    base_url=ai_url)

async def get_pray_response(request:PrayResponseRequest) -> str:
    """
        Gets response for prayer from AI

    """
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": pray_prompt},
            {"role": "user", "content": request.model_dump_json()}
        ],
        temperature= pray_temperature
    )
    return response.choices[0].message.content

async def get_analysis_response(data:UserData) -> AIResponse:
    """
        Gets instruction based on player's actions for plugin

    """
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": analysis_prompt},
            {"role": "system", "content": "Schema of your response:" + str(AIResponse.model_json_schema())},
            {"role": "user", "content": data.model_dump_json()}
        ],
        temperature= analysis_temperature,
        response_format={"type": "json_object"}
    )
    return AIResponse.model_validate_json(response.choices[0].message.content)
