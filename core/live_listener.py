import speech_recognition as sr

recognizer = sr.Recognizer()

# ==========================================
# LIVE LISTEN FUNCTION
# ==========================================

def listen_once():

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

            command = recognizer.recognize_google(
                audio
            )

            return command.lower()

    except:

        return None