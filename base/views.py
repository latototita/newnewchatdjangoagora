from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm

# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "014a1c5003a54d1aa470493990405207"
    appCertificate = "f4b72a52122e4242874a4fb431097340"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
@login_required
def dashboard(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
    else:
        user=None
    context={'user':user}
    return render(request,'base/profile.html',context)



# Create your views here.
def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            request.session['customer'] = user.id
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                messages.success(request, f'Welcome, {username}.You have Signed In Successfully')
                return redirect('dashboard')
        else:
            messages.success(request, 'Username or Password Incorrect!')
            context={}
            return render(request,'sign-in.html',context)
    context={}
    return render(request,'sign-in.html',context)
def signup(response):
    if response.method=="POST":
        form=CustomUserCreationForm(response.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                messages.success(response, f'Email already in use, Please use a different Email')
                return render(response,'signup.html',)
            elif User.objects.filter(username=form.cleaned_data['username']):
                messages.success(response, f'Username already in use, Please use a different Username')
                return render(response,'signup.html',)
            form.save()
            messages.success(response, f'Successfully Registered,Please log into your Account to Make Orders')
            return redirect('login')
    else:
        form=CustomUserCreationForm()
    context={'form':form}
    return render(response,'sign-up.html',context)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    messages.success(request, 'You have Signed Out Successfully')
    return redirect('profile')
