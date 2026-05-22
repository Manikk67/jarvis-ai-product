import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

engine.setProperty('rate', 170)

def speak(text):

    print(f"\n🤖 Jarvis: {text}")

    engine.say(text)

    engine.runAndWait()

def take_command():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            command = recognizer.recognize_google(audio)

            print(f"\n🧠 You: {command}")

            return command.lower()

        except sr.WaitTimeoutError:

            print("⌛ Listening timeout...")

            return ""

        except sr.UnknownValueError:

            print("❌ Could not understand.")

            return ""

        except sr.RequestError:

            print("🌐 Internet error.")

            return ""

        except Exception as e:

            print(f"⚠️ Error: {e}")

            return ""