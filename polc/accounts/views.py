# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import DetailView

from .forms import SignUpForm
from .models import UserProfile

# from .models import Profile
# from .tokens import account_activation_token



@login_required
def settings(request):
    user = request.user
    print ("user", user)

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# this is adding the user profile for users using the site
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

User = get_user_model()

class UserDetailView(DetailView):
    template_name = 'registration/user_detail.html'
    queryset = User.objects.all()
    
    def get_object(self):
        return get_object_or_404(
                    User, 
                    username__iexact=self.kwargs.get("username")
                    )
    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        context['following'] = following
        context['recommended'] = UserProfile.objects.recommended(self.request.user)
        return context






# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate Your MySite Account'
#             message = render_to_string('registration/account_activation_email.html', {
#                 'user': user,
#                 'domain': 'localhost/',
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('accounts:account_activation_sent')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})




# def account_activation_sent(request):
#     return render(request, 'registration/account_activation_sent.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.profile.email_confirmed = True
#         user.save()
#         login(request, user)
#         return redirect('home')
#     else:
#         return render(request, 'registration/account_activation_invalid.html')





# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})



# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})


