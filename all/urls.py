from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/signup',views.Signup.as_view(),name="api_signup"),
    path('signup/',views.sign_up,name="signup"),
    path('verify/',views.verify,name="verify"),
    path('activate/<str:uidb64>/<str:token>/',views.activate,name="activate"),
]
