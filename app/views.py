from django.shortcuts import render,redirect
from .forms import*
# for pdf
from django.conf import settings
from urllib.parse import urlparse, urlunparse
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from school.utils import render_to_pdf #created in step 4
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from urllib.parse import urlparse, urlunparse

# Create your views here.



@login_required
def database_function(request, event_type):
    if request.method == 'POST':
        data = database_form(request.POST)
        print(data)
        if data.is_valid():            
            data.save()
            return redirect('/')
    else:
        data=database_form()
        data.event_type = event_type
        data.__init__()
    return render(request,'registeration_page.html',{'ob':data})

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        context = {
            'today': 'Mayur',
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


def submit(request):
    if request.method=='POST':
        frm = visitor_form(request.POST)
        if frm.is_valid():
            print("Hello")
            frm.save()
            return redirect('/')
    else:
        frm= visitor_form()
    return render(request,"index.html", {'e': frm})

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


def login_user(request):
    if request.method == 'POST':
        user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password')
            )
        login(request, user)
        return render(request, 'index.html')
    else:
        return HttpResponse("Error") 

def signup(request):
    if request.method == 'POST':
        form = Regforms(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username,password=password,email=email)
            user = authenticate(username=username,password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = Regforms()
    if request.user.is_authenticated:    
        return redirect('/')
    else:    
        return render(request, "sign-up.html",{'form':form})

def home(request):
    return render(request, 'index.html')

def blogs(request):
    return render(request,'blog-details.html')

# def password_reset(request):
#     return render(request,'password_reset_form.html')

# # def password_reset_done(request):
# #     return render(request,'password_reset_done.html')

# def password_reset_confirm(request):
#     return render(request,'password_reset_confirm.html')

def google_verification(request):
    return render(request,'googlecca9cc668fcf9c62.html')



class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context



class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password-reset-done')
    template_name = 'password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'password_reset_done.html'
    title = _('Password reset sent')

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password-reset-complete')
    template_name = 'password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

def PasswordResetCompleteView(request):
    return render(request,'password-reset-complete.html')



@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        google_login = user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'index.html', {
        'github_login': github_login,
        'google_login': google_login,
        'facebook_login': facebook_login,
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
    return render(request, 'password_reset.html', {'form': form})
