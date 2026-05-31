from groq import Groq

import config

client = Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None


def ask_ai(prompt: str) -> str:
    if not client:
        return (
            "AI is not configured. Add GROQ_API_KEY to your .env file "
            "(see .env.example)."
        )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are {config.ASSISTANT_NAME}, a concise productivity "
                        f"assistant for {config.USER_NAME}. Be helpful and direct."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as exc:
        return f"AI Error: {exc}"
