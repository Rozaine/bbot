import openai
from openai import AsyncOpenAI

import config

client = AsyncOpenAI(
    api_key=config.API_KEY_OPENAI,
    base_url="https://api.proxyapi.ru/openai/v1",
)


async def get_embedding(text_or_tokens, model=config.EMBEDDING_MODEL):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Ты библиотекарь, ты знаешь все о книгах и советуешь книги, которые тебя присят"
                           "Ничего кроме как советовать книги ты не можешь"
                           "Отвечай как можно короче"
            },
            {
                "role": "user",
                "content": text_or_tokens,
            },
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content
