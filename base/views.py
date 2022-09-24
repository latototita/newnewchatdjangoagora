from django.shortcuts import render,redirect
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
import os
import time
import json

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from pusher import Pusher

 
# Instantiate a Pusher Client
pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
                       key=os.environ.get('PUSHER_KEY'),
                       secret=os.environ.get('PUSHER_SECRET'),
                       ssl=True,
                       cluster=os.environ.get('PUSHER_CLUSTER')
                       )

# Create your views here.

def lobby(request):
    context={'conference':'conference'}
    return render(request, 'base/lobby.html',context)

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


@login_required(login_url='base:login')
def dashboard(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
    else:
        user=None

    all_users = User.objects.all()#exclude(id=request.user.id).only('id', 'username')
    user=User.objects.get(id=request.user.id)
    image=user.image
    context={'image':image,'user':user,'allUsers': all_users}
    
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
                return redirect('base:dashboard')
        else:
            messages.success(request, 'Username or Password Incorrect!')
            context={}
            return render(request,'base/sign-in.html',context)
    context={}
    return render(request,'base/sign-in.html',context)

DEFAULT = '/static/default.jpg'
def signup(response):
    if response.method=="POST":
        form=RegistrationForm(response.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                messages.success(response, f'Email already in use, Please use a different Email')
                return render(response,'signup.html',)
            elif User.objects.filter(username=form.cleaned_data['username']):
                messages.success(response, f'Username already in use, Please use a different Username')
                return render(response,'signup.html',)

            feed_back=form.save(commit=False)
            feed_back.image=DEFAULT
            feed_back.save()
            messages.success(response, f'Successfully Registered,Please log into your Account to Make Orders')
            return redirect('base:login')
    else:
        form=RegistrationForm()
    context={'form':form}
    return render(response,'base/sign-up.html',context)


@login_required(login_url='base:login')
def Logout(request):
    logout(request)
    messages.success(request, 'You have Signed Out Successfully')
    return redirect('profile')

@login_required(login_url='base:login')
def changepic(request):
    form=ProfilePicForm()
    if response.method=="POST":
        form=ProfilePicForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully Registered,Please log into your Account to Make Orders')
            return redirect('dashboard')
        else:
            messages.success(request, f'Form Invalid')
            return redirect('changepic')
    
    context={'form':form}
    return render(response,'base/change.html',context)

'''
def search_user(request):
    if request.method=="POST":
        searched=request.POST['searched']
        try:
            multiple_q=Q(Q(username__icontains=searched))
            users_present=User.objects.filter(multiple_q).order_by('?')

    '''



#@login_required(login_url='base:login')
def index(request):
    User = get_user_model()
    all_users = User.objects.exclude(id=request.user.id).only('id', 'username')
    context={'allUsers': all_users,'call':'call'}
    return render(request, 'base/lobby.html', context)


def pusher_auth(request):
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.username
            }
        })
    return JsonResponse(payload)


def generate_agora_token(request):
    appID = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = json.loads(request.body.decode(
        'utf-8'))['channelName']
    userAccount = request.user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    return JsonResponse({'token': token, 'appID': appID})


def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = request.user.id

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channelName': channel_name,
            'from': caller
        }
    )
    return JsonResponse({'message': 'call has been placed'})



def terms(request):
    context={}
    return render(request, 'base/terms.html', context)
