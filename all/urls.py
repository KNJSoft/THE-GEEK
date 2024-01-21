from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/post/signup',views.Signup.as_view(),name="api_signup"),
    path('api/post/signin',views.Signin.as_view(),name="api_signin"),
    path('signup/',views.sign_up,name="signup"),
    path('verify/',views.verify,name="verify"),
    path('email/',views.email,name='email'),
    path('messages/',views.notification,name="notification"),
    path('profile/',views.profile,name='profile'),
    path('activate/<str:uidb64>/<str:token>/',views.activate,name="activate"),
    path('logout/',views.log_out,name='logout')
]
