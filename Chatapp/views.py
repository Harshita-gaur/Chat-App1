from django.http import JsonResponse
from .models import ChatMessage
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Q

def logout_view(request):
    logout(request)
    return redirect('home')  

# views.py
from django.shortcuts import render, redirect
from .models import ChatMessage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')  

        try:
            receiver = User.objects.get(id=receiver_id)
            message = ChatMessage.objects.create(sender=request.user, receiver=receiver, content=content)
            message.save()
            return JsonResponse({'message': message.content, 'sender': message.sender.username, 'timestamp': message.timestamp})

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return redirect('chat')  




@login_required
def chat(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat.html', {
        'users': users,
        'receiver': None,  
    })


@login_required
def chat_with_user(request, receiver_id):
    try:
        receiver = User.objects.get(username=receiver_id)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=receiver) | 
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages,
    })



@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat') 
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, 'index.html', {'error': 'Invalid credentials'})
    return render(request, 'index.html')  


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please try another one.")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Signup successful! Please login to continue.")
            return redirect('login_user')
    
    return render(request, 'index.html')



def home(request):
    return render(request, 'index.html')


def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        return JsonResponse({'status': 'success', 'message': message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
