from typing import Any
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import logout, update_session_auth_hash
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms

class CreateAccountView(FormView):
    form_class = forms.CreateAccountForm
    template_name = 'create_account.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Check your email address for verification.')
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_link = f"https://listlyflow.onrender.com/user/activate/{uid}/{token}"
        subject = "Very Email"
        email_body = render_to_string('verify_email.html', {'verify_link': verify_link})
        email = EmailMultiAlternatives(subject,'', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return super().form_valid(form)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('create-account')
    
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        messages.success(self.request, 'Login successful')
        return reverse_lazy('home')
    def form_invalid(self, form):
        messages.success(self.request, 'Invalid username or password.')

@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout successful')
    return redirect('home')

class UserProfileView(UpdateView, LoginRequiredMixin):
    model = User
    from_class = UserChangeForm
    fields = ('first_name','last_name')
    pk_url_kwarg = 'id'
    template_name = 'profile.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)
        

class ContactUsView(FormView):
    form_class = forms.ContactUsForm
    template_name = "contact_us.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thanks for reaching out to us. We will get back to you soon.')
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin,View):
    template_name = "password_change.html"
    
    def get(self, request):
        user = request.user
        form = SetPasswordForm(user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Changed password successfully.")
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return render(request, self.template_name, {'form': form})
                             

