from config import api_key
import speech_recognition as sr
import requests
import time


class GPT_api:
    def __init__(self):
        self.engine = "gpt-3.5-turbo"

    def chat_text(self, message):
        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            param = {
                      "model": self.engine,
                      "messages": [{"role": "user", "content": message}]
                    }

            proxies = {
                'https': 'your_proxies'
            }

            ask = requests.post("https://api.openai.com/v1/chat/completions", headers=header, json=param, proxies=proxies).json()
            
            return ask['choices'][0]['message']['content']

        except Exception as e:
            print(e)
            return "Ошибка! Попробуйте еще раз!"


    def chat_audio(self, audio_name):

        process = subprocess.run(['ffmpeg', '-i', audio_name, f"{audio_name.split('.')[0]}.wav", "-y"])
        time.sleep(3)

        try:
            r = sr.Recognizer()
            file = sr.AudioFile(f"{audio_name.split('.')[0]}.wav")
            with file as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
                result = r.recognize_google(audio, language="ru")


            return self.chat_text(result)

        except Exception as e:
            return "Ошибка! Попробуйте еще раз!"


gpt = GPT_api()

