from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.conf import settings
from json import loads, JSONDecodeError
from pytube import YouTube

import assemblyai as aai
import os


# getting title and audio from youtube
class YT:
    def __init__(self, link):
        self.yt = YouTube(link)

    def title(self):
        return self.yt.title
    
    def download(self):
        file = self.yt.streams.filter(only_audio=True).first()
        file = file.download(settings.MEDIA_ROOT)
        name, ext = os.path.splitext(file)
        audio = name + '.mp3'
        os.rename(file, audio)
        return audio


# get video transcript
def get_transcript(link):
    yt = YT(link)
    audio_file = yt.download()
    pass

# blog generator view
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            link = data['link']
            # return JsonResponse({'content': link})
        
        except (KeyError, JSONDecodeError):
            return JsonResponse({'error': 'Invalid data!!!'}, status=400)

        yt = YT(link)
        title = yt.title()
        

    else:
        return JsonResponse({'error': 'Invalid request method!!!'}, status=405)

# home view
@login_required(login_url='login_')
def homepage(request):
    return render(request, 'app/index.html')

# signup view
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('home')
            
            except:
                error_message = 'Error creating account'
                context = {'error_message': error_message}
                return render(request, 'app/signup.html', context)

        else:
            error_message = 'Password do not match'
            context = {'error_message': error_message}
            return render(request, 'app/signup.html', context)
        
    return render(request, 'app/signup.html')

# login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        userr = authenticate(request, username=username, password=password)

        if userr:
            login(request, userr)
            return redirect('home')
        
        else:
            error_message = 'Account not found'
            context = {'error_message': error_message}
            return render(request, 'app/login.html', context)

    return render(request, 'app/login.html')


def all_blogs(request):
    pass


def blog_details(request):
    pass

# logout view
def user_logout(request):
    logout(request)
    return redirect('login_')