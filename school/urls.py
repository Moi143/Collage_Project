from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from app.views import*
from app.views import GeneratePdf
from django.conf.urls import include
from app.views import signup,settings,home,password,logout_user, login_user,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('register_form/<str:event_type>',database_function, name="register_form"),
    path('Details',GeneratePdf.as_view()),
    path('',home),
    path('a',submit),
    path('', home, name='home'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup, name='signup_student'),
    path('settings/', settings, name='settings'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('b',blogs),
    path('password-reset/',PasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password-reset-confirm'),
    path('password-reset/complete/',PasswordResetCompleteView,name='password-reset-complete'),
    path('googlecca9cc668fcf9c62.html',google_verification),

 
]
urlpatterns += staticfiles_urlpatterns()
