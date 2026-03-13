from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=""
)


async def generate_seo_explanation(url: str, metrics: dict, score: int):

    prompt = f"""
Ты эксперт по SEO и производительности сайтов.

Проанализируй Core Web Vitals сайта.

URL: {url}

Performance score: {score}

Метрики:
{metrics}

Объясни простым языком для человека без SEO знаний:

1. Что означает каждая метрика
2. Хороший ли результат
3. Какие проблемы есть
4. Как их исправить
5. Как это влияет на SEO

Ответ структурируй так:

## Общая оценка
## Объяснение метрик
## Основные проблемы
## Рекомендации
"""

    response = client.chat.completions.create(
        model="stepfun/step-3.5-flash:free",
        messages=[
            {
                "role": "system",
                "content": "Ты профессиональный SEO аналитик."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        extra_body={
            "reasoning": {"enabled": True}
        }
    )

    return response.choices[0].message.content