from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import uuid
from . models import PasswordResetToken,Profile
from . sendmail import send_forget_password_mail
from . models import Movie,PaymentStatus
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    movies=Movie.objects.all()
    profiles=Profile.objects.filter(user=request.user)

    return render(request, 'home.html',{'movies':movies,'profiles':profiles})
def SingleVideoPost(request,uuid):
    
    movie = get_object_or_404(Movie, uuid=uuid)
    videos = movie.videos.all()  
    


    return render(request, 'singleVideoPost.html',{'movie':movie,'videos':videos})

def handleSignUp(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        PaymentStatus.objects.create(user=user)
        messages.success(request, 'signup_success')

        return redirect('subscription')
        # return redirect('login')
    return render(request,'signup.html')

def handleLogin(request):
   
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
       

        if user is not None:
            
            login(request,user)
            if user.paymentstatus.is_paid:
                
                return redirect('profile')
            else:
                return redirect('subscription')
            
        
        else:
            messages.success(request,'invalid username or password')
            return render(request,'login.html')



    return render(request,'login.html')
@csrf_exempt
def subscription_plan(request):
    if request.user.is_authenticated and not request.user.paymentstatus.is_paid:
        return render(request, 'subscription.html')
    if messages.get_messages(request):
        for message in messages.get_messages(request):
            if message.message == 'signup_success':
                messages.success(request,'s')
                return render(request, 'subscription.html')
            
    else:
        return HttpResponse("404 not found")
    return render(request,'subscription.html')

    
@csrf_exempt
def handle_payment(request):
    
    price=0
    if request.method=="POST":
        user = request.user
        if 'basic' in request.POST:
            print("hello word")
            price=999            
        if 'standard' in request.POST:
            print("hello nepal")
            price=1500
        
            
        if 'premium' in request.POST:
            price=2000
            print("premium")
        
        user.paymentstatus.is_paid = True
        user.paymentstatus.save()
    else:
        return HttpResponse("404 not found")
        

    return render(request,'payment.html',{'price':price})
   

def forgot_password(request):
    if request.method=="POST":
        username=request.POST.get('username')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'username doesnot exist')
            return redirect('forgot_password')
        else:
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            PasswordResetToken.objects.create(user=user_obj, token=token)
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'Password reset email has been sent')
            return redirect('forget_password')



    return render(request,'forget_password.html')


def change_password(request,token):
    reset_token = PasswordResetToken.objects.get(token=token)
    if request.method=="POST":
        new_password=request.POST.get('pass1')
        confirm_password=request.POST.get('pass2')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'change_password.html', {'token': token})

        user = reset_token.user
        user.set_password(new_password)
        user.save()
        reset_token.delete()
        messages.success(request, 'Password has been reset successfully')
        return redirect('login')

    return render(request,'change_password.html')


def esewa_request(request):
    return render(request,'esewa_request.html')


def practice(request):
    return render(request,'practice.html')

def slider(request):
    movies=Movie.objects.all()
    return render(request,'slider.html',{'movies':movies})

def handleSearch(request):
    query=request.GET.get('query')
    movies=Movie.objects.filter(title__icontains=query)

    return render(request,'search.html',{'movies':movies})

def handleLogout(request):
    if request.method=="POST":
        logout(request)
        print("hello world")
        return redirect('login')
    else:
        return HttpResponse("404 not found")

def index(request):
    return render(request,'index.html')


def profile(request):
    profiles=Profile.objects.filter(user=request.user)
    if not profiles:
        return render(request,'create_profile.html')


    return render(request,'profile.html',{'profiles':profiles})
    # if request.user.is_authenticated:
    #     profiles = Profile.objects.filter(user=request.user)
    #     if not profiles:
    #         return render(request, 'create_profile.html')
    #     else:

    #         return render(request, 'profile.html', {'profiles': profiles})
    # else:
    #     return render(request, 'create_profile.html')  # or redirect to a login page
@csrf_exempt
def create_profile(request):
    if request.method=="POST":
        user=User.objects.get(username=request.user)
        profile_name=request.POST.get('profile_name')
        image=request.FILES['profile_image']
        Profile.objects.create(user=user,name=profile_name,image=image)
        return redirect('profile')


    return render(request,'create.html')


def profile_detail(request,id):
    return render(request,'profile_detail.html')

def manage_profile(request):
    profiles=Profile.objects.filter(user=request.user)
    return render(request,'manage_profile.html',{'profiles':profiles})
@csrf_exempt
def edit_profile(request,id):
    profile=Profile.objects.get(id=id)
    if request.method=="POST":  
        if 'save' in request.POST:
            profile.name=request.POST['name']
            profile.save()
            return redirect('manage_profile')
        if 'cancel' in request.POST:
            return redirect('manage_profile')
        if 'delete' in request.POST:
            profile.delete()
            return redirect('manage_profile')
            

        
    return render(request,'edit_profile.html',{'profile':profile})


def transfer_profile(request):
    return render(request,'transfer_profile.html')

def home_page(request):
    return render(request,'homepage.html')
