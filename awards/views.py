from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('awards')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def home(request):
    
    try:
        all_posts = Blog.objects.all()
        print(all_posts)
        
    except Blog.DoesNotExist:
        all_posts = None

    return render(request, 'index.html', {'all_posts': all_posts})

@login_required(login_url='login')
def awards(request):
    return render (request, 'projects/awards.html')

@login_required(login_url='login')
def profile(request):
    current_user = request.user
    profile = Profile.objects.all()

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=request.user)
        p_form = UpdateUserProfileForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            
            return render(request,'registration/profile.html')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateUserProfileForm(instance=request.user.profile)


    context = {
        'u_form':u_form,
        'p_form':p_form,
    }

    return render(request, 'registration/profile.html',locals())

@login_required(login_url='login')
def posts(request):
    captions = Blog.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = UploadForm()
    params={
        'captions': captions,
        'form': form,
        'users': users,
    }

    return render(request, 'projects/post.html',params)

def success(request): 
    return HttpResponse('successfully uploaded') 

@login_required(login_url='login')
def search_blog(request):
    if 'q' in request.GET and request.GET['q']:
        name = request.GET.get("q")
        details = Blog.objects.filter(name__icontains=name)
        message = f'name'
        params = {
            'details': details,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any project"
    return render(request, 'search.html', {'message': message})