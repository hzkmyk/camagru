from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import File
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import NotificationForm, SignupForm, UploadPicForm
from .tokens import account_activation_token
from .models import Image, Comment, Profile
import re, io
import base64
from django.http.response import JsonResponse

def home(request):
    image_list = Image.objects.all().order_by('-uploaded_at')
    paginator = Paginator(image_list, 10)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    return render(request, 'home.html', {'images': images})

@login_required
def delete(request,pk):
    image = Image.objects.get(pk=pk)
    image.delete()
    return redirect('mypage')

@login_required
def like(request,pk):
    image = Image.objects.get(pk=pk)
    image.num_likes += 1
    image.save()
    return redirect('home')

# def api_like(request,pk):
#     image = Image.objects.get(pk=pk)
#     image.num_likes += 1
#     image.save()
#     return JsonResponse({"like": image.num_likes})

@login_required
def mypage(request):
    image_list = Image.objects.filter(user=request.user).order_by('-uploaded_at')
    paginator = Paginator(image_list, 10)

    page = request.GET.get('page')
    images = paginator.get_page(page)
    return render(request, 'mypage.html', {'images': images}) 

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadPicForm(request.POST, request.FILES)
        form.fields['image_field'].widget = forms.HiddenInput()
        if form.is_valid():
            ImageCaption = request.POST.get('caption_field')
            if request.FILES:
                ImageFile = request.FILES['file_field']
            else:
                dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
                ImageData = request.POST.get('image_field')
                ImageData = dataUrlPattern.match(ImageData).group(2)
                if  ImageData == None or len(ImageData) == 0:
                    pass
                ImageData = base64.b64decode(ImageData)
                ImageFile = File(io.BytesIO(ImageData))
            image = Image(image=ImageFile, user=request.user, caption=ImageCaption)
            image.image.save('screenshot.jpg', ImageFile, save=True)
            return redirect('home')
    else:
        form = UploadPicForm()
        form.fields['image_field'].widget = forms.HiddenInput()
    return render(request, 'upload.html', {'form': form})

@login_required
def comment(request):
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            pk = request.POST.get('imageid')
            image = Image.objects.get(pk=pk)
            image_owner = image.user
            if image_owner.profile.email:
                mail_subject = 'Camagru: You received a comment on your post'
                message = render_to_string('commentreceived.html', {
                    'user': image.user,
                })
                to_email = image_owner.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
            comment = Comment.objects.create(text=text, user=request.user, image=image)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Camagru: E-mail Verification'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'confirm.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def notifications(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            prof = Profile.objects.get(user=request.user)
            prof.email = form.cleaned_data['notification']
            prof.save()
    else:
        form = NotificationForm()
    return render(request, 'notifications.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'success.html')
    else:
        return HttpResponse('Activation link is invalid!')
