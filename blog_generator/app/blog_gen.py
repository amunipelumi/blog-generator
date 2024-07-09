from django.conf import settings as st
from pytube import YouTube
from .config import settings

import assemblyai as aai
import openai
import os



# getting title, audio and transcript from youtube
class BlogGen:
    def __init__(self, link):
        self.yt = YouTube(link)

    def title(self):
        return self.yt.title
    
    def download(self):
        file = self.yt.streams.filter(only_audio=True).first()
        file = file.download(st.MEDIA_ROOT)
        name, ext = os.path.splitext(file)
        audio = name + '.mp3'
        os.rename(file, audio)
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
    
    # generating blog through openai
    def blog_from_ai(self, text):
        openai.api_key = settings.openai_key
        prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{text}\n\nArticle:"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )

        content = response.choices[0].text.strip()
        return content
