from groq import Groq

from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def ask_ai(prompt):

    if not client:

        return (
            "AI is not configured. Add your GROQ_API_KEY to a .env file "
            "(see .env.example)."
        )

    try:

        chat_completion = client.chat.completions.create(

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are Jarvis, a futuristic AI assistant for Mani. "
                    "You are smart, helpful, futuristic, and concise."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            model="llama-3.1-8b-instant"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:

        return f"AI Error: {e}"