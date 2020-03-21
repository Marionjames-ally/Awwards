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

@login_required(login_url='login')
def rating(request, post):
    post = Blog.objects.get(name=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'projects/rating.html', params)