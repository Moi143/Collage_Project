from django import forms
from .models import*
from datetime import date
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import (authenticate, get_user_model, password_validation,)


class database_form(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(database_form, self).__init__(*args, **kwargs)
		try:	
			self.fields['event'].queryset = event.objects.filter(event_type = self.event_type)
		except:
			pass	

	class Meta:
		model=database
		fields= '__all__'

class visitor_form(forms.ModelForm):
	class Meta:
		model= visitor
		fields= '__all__'

class sign_form(forms.ModelForm):
	class Meta:
		model= signup
		fields= '__all__'

class event_type_form(forms.ModelForm):
	class Meta:
		model = event
		fields = "__all__"


class Regforms(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)

    email=forms.CharField(widget=forms.EmailInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)

    password=forms.CharField(widget=forms.PasswordInput
                             (attrs={'class':'form-control'}),
                             max_length=30,
                             required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput
                            (attrs={'class': 'form-control'}),
                            label="Confirm your password",
                            max_length=30,
                            required=True)
    class Meta:
        model=User
        fields=['username','email','password','confirm_password',]

UserModel = get_user_model()


# class PasswordResetForm(forms.Form):
#     email = forms.EmailField(label=_("Email"), max_length=254)

#     def send_mail(self, subject_template_name, email_template_name,
#                   context, from_email, to_email, html_email_template_name=None):
#         """
#         Send a django.core.mail.EmailMultiAlternatives to `to_email`.
#         """
#         subject = loader.render_to_string(subject_template_name, context)
#         # Email subject *must not* contain newlines
#         subject = ''.join(subject.splitlines())
#         body = loader.render_to_string(email_template_name, context)

#         email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
#         if html_email_template_name is not None:
#             html_email = loader.render_to_string(html_email_template_name, context)
#             email_message.attach_alternative(html_email, 'text/html')

#         email_message.send()

#     def get_users(self, email):
#         """Given an email, return matching user(s) who should receive a reset.

#         This allows subclasses to more easily customize the default policies
#         that prevent inactive users and users with unusable passwords from
#         resetting their password.
#         """
#         active_users = UserModel._default_manager.filter(**{
#             '%s__iexact' % UserModel.get_email_field_name(): email,
#             'is_active': True,
#         })
#         return (u for u in active_users if u.has_usable_password())

#     def save(self, domain_override=None,
#              subject_template_name='password_reset_subject.txt',
#              email_template_name='password_reset_email.html',
#              use_https=False, token_generator=default_token_generator,
#              from_email=None, request=None, html_email_template_name=None,
#              extra_email_context=None):
#         """
#         Generate a one-use only link for resetting password and send it to the
#         user.
#         """
#         email = self.cleaned_data["email"]
#         for user in self.get_users(email):
#             if not domain_override:
#                 current_site = get_current_site(request)
#                 site_name = current_site.name
#                 domain = current_site.domain
#             else:
#                 site_name = domain = domain_override
#             context = {
#                 'email': email,
#                 'domain': domain,
#                 'site_name': site_name,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'user': user,
#                 'token': token_generator.make_token(user),
#                 'protocol': 'https' if use_https else 'http',
#                 **(extra_email_context or {}),
#             }
#             self.send_mail(
#                 subject_template_name, email_template_name, context, from_email,
#                 email, html_email_template_name=html_email_template_name,
#             )


# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     new_password1 = forms.CharField(
#         label=_("New password"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label=_("New password confirmation"),
#         strip=False,
#         widget=forms.PasswordInput,
#     )

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         password_validation.validate_password(password2, self.user)
#         return password2

#     def save(self, commit=True):
#         password = self.cleaned_data["new_password1"]
#         self.user.set_password(password)
#         if commit:
#             self.user.save()
#         return self.user
