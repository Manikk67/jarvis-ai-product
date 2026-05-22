import random

def get_offline_response(command):

    command = command.lower()

    # GREETINGS
    if "hello" in command or "hi" in command:

        return "Hello Mani. How can I assist you today?"

    # WHO ARE YOU
    elif "who are you" in command:

        return "I am Jarvis, your personal AI assistant."

    # MOTIVATION
    elif "motivate me" in command:

        motivations = [

            "Success comes from consistency.",

            "Small daily progress creates big success.",

            "Discipline is more powerful than motivation.",

            "Focus now. Your future self will thank you."
        ]

        return random.choice(motivations)

    # JOKES
    elif "joke" in command:

        jokes = [

            "Why do programmers hate nature? Too many bugs.",

            "Why did Python go to therapy? Too many exceptions.",

            "Debugging is like being a detective where you are also the murderer."
        ]

        return random.choice(jokes)

    # DEFAULT
    else:

        return "Sorry Mani, I don't understand that yet."