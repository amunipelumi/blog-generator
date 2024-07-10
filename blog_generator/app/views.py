from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import reverse
from json import loads, JSONDecodeError
from .blog_gen import BlogGen



# blog generator view
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = loads(request.body)
            link = data['link']
        
        except (KeyError, JSONDecodeError):
            return JsonResponse({'error': 'Invalid data..'}, status=400)

        bg = BlogGen(link)
        title = bg.title()
        transcript = bg.get_transcript()
        if transcript == None:
            return JsonResponse({'error': 'Unable to get transcript..'}, status=500)
        return JsonResponse({'title': title, 'article': transcript})
    
        blog_article = bg.blog_from_ai(transcript)
        if blog_article:
            return JsonResponse({'title': title, 'article': blog_article})
        
        return JsonResponse({'error': 'Error occured while generating blog..'}, status=500)
        
    return JsonResponse({'error': 'Invalid request method..'}, status=405)

# home view
@login_required(login_url='login_')
def homepage(request):
    g_url = reverse('blog_gen_')
    context = {
        'csrf_token': request.COOKIES.get('csrftoken'),
        'g_url': g_url,
    }
    return render(request, 'app/index.html', context)

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


# https://www.youtube.com/shorts/DIfZ94D796I
# https://www.youtube.com/watch?v=IZsQqarWXtY
# https://www.youtube.com/watch?v=VmNhDUKMHd4