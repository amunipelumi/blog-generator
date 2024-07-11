from django.conf import settings as st
from pytube import YouTube
from groq import Groq
from .config import settings

import assemblyai as aai
import os



# getting title, audio and transcript from youtube
class BlogGen:
    def __init__(self, link):
        self.yt = YouTube(link)
        self.client = Groq(api_key=settings.groq_key)

    def title(self):
        return self.yt.title
    
    def download(self):
        try:
            file = self.yt.streams.filter(only_audio=True).first()
            file = file.download(st.MEDIA_ROOT)
            name, ext = os.path.splitext(file)
            audio = name + '.mp3'
            os.rename(file, audio)
        except FileExistsError:
             pass
        return audio

    def get_transcript(self):
        audio_file = self.download()
        aai.settings.api_key = settings.api_key
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)

        if transcript.status == aai.TranscriptStatus.error:
                print(transcript.error)
                return None

        return transcript.text
    
    # generating blog through ai
    def blog_from_ai(self, text):
        prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article and do not include a title, just the the body:\n\n{text}"
    
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                # {
                #     "role": "system",
                #     "content": "JSON"
                # },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1000,
        )

        article = response.choices[0].message.content
        # print(type(article))
        return article
 