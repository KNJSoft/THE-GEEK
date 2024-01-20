from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Notification, MonModeleEmail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .fonctions import *
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken

# Create your views here.

#
# @login_required
# def create_notification(request, message):
#     notification = Notification(user=request.user, message=message)
#     notification.save()
#     # Code supplémentaire pour envoyer la notification en push, par exemple en utilisant Django Channels
#     return render(request, 'notification.html', {'notification': notification})
#
# @login_required
# def view_notifications(request):
#     notifications = Notification.objects.filter(user=request.user, is_read=False)
#     return render(request, 'all/notification.html', {'notifications': notifications})
#

def index(request):
    return render(request,"all/index2.html")


class Signup(APIView):
    def post(self,request):
        username=request.data.get('username')
        #nom = request.data.get('nom')
        #prenom = request.data.get('prenom')
        email = request.data.get('email')
        password = request.data.get('password')
        cpassword = request.data.get('cpassword')
        if not username or not  email or not password or not cpassword:
            return Response({'error':'les champs sont obligatoire'},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(username) > 10:
            return Response({'error': "SVP le nom d'utilisateur ne doit pas dépassé 10 caractères."},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(username) < 5:
            return Response({'error': "SVP le nom d'utilisateur doit avoir au moins 5 caractères."},
                            status=status.HTTP_400_BAD_REQUEST)
        if password <12:
            return Response({'error': 'le mot de passe doit avoir au moins 12 caracteres'},
                            status=status.HTTP_400_BAD_REQUEST)
        if password_verify(password):
            return Response({'error': "le mot de passe doit avoir au moins une lettre maj, min, un chiffre, un carac special et pas d'espace"},
                            status=status.HTTP_400_BAD_REQUEST)
        if password != cpassword:
            return Response({'error': 'le mot de passe ne correspond pas!'},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username):
            return Response({'error':'lutilisateur existe deja'},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email):
            return Response({'error': 'Cet adresse email est déjà associé à un compte.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            my_user = User.objects.create_user(username, email, password)
            # my_user.first_name = prenom
            # my_user.last_name = nom
            my_user.is_active = False
            my_user.save()
            message = f"Salut {username} bienvenue sur THE-GEEK, la nouvelle plateforme du E-learning."
            notification = Notification(user=my_user, message=message, is_read=False)
            notification.save()
            # send mail confirm
            current_site = get_current_site(request)
            destinataires = [my_user.email, ]
            sujet = 'Confirmation de votre email'
            # corps = 'Contenu de l\'email'

            context = {
                'user': my_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
                'token': generateToken.make_token(my_user)
            }
            contenu_html = render_to_string('all/emailConfimation.html', context)
            email = MonModeleEmail(sujet, contenu_html, destinataires)
            email.content_subtype = "html"
            email.send()

        except:
            return Response({'error':"Erreur inconnue, reessayer"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'INSCRIPTION REUISSI'},
                        status=status.HTTP_201_CREATED)

def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['prenom']
        lastname = request.POST['nom']
        email = request.POST['email']
        password = request.POST['mdp']
        confirmpwd = request.POST['pwd']
        if User.objects.filter(username=username):
            messages.add_message(request, messages.ERROR, "Ce nom d'utilisateur existe déjà essayer un autre.")
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})
        if User.objects.filter(email=email):
            messages.add_message(request, messages.ERROR, 'Cet adresse email est déjà associé à un compte.')
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})
        if len(username) > 10:
            messages.add_message(request, messages.ERROR, "SVP le nom d'utilisateur ne doit pas dépassé 10 caractères.")
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})
        if len(username) < 5:
            messages.add_message(request, messages.ERROR, "SVP le nom d'utilisateur doit avoir au moins 5 caractères.")
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})

        if password != confirmpwd:

            messages.add_message(request, messages.ERROR, 'le mot de passe ne correspond pas! ')
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        message=f"Salut {username} bienvenue sur THE-GEEK, la nouvelle plateforme du E-learning."
        notification=Notification(user=my_user,message=message,is_read=False)
        notification.save()
        current_site = get_current_site(request)
        destinataires = [my_user.email,]
        sujet = 'Activation de votre compte-THE-GEEK'
        # corps = 'Contenu de l\'email'

        context = {
            'user': my_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user)
        }
        contenu_html = render_to_string('all/emailConfimation.html', context)
        email = MonModeleEmail(sujet, contenu_html, destinataires)
        email.content_subtype = "html"
        try:
            email.send()
        except:
            messages.add_message(request, messages.ERROR, "Erreur inconnue, reessayer.")
            return render(request, "all/sign_up.html", {"msg": messages.get_messages(request)})

    return render(request, 'all/sign_up.html')

@require_GET
def verify(request):
    username=request.GET.get('username',None)
    email=request.GET.get('email',None)
    if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():

        data={
            "existe": True
        }
    elif User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        data = {
            "existe": True
        }
    elif username=="" and email=="" :
        data = {
            "existe": True
        }
    elif username=="" or email=="" :
        data = {
            "existe": True
        }
    else:
        data = {
            "existe": False
        }
    return JsonResponse(data)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active  = True
        my_user.save()
        message = f"Salut {my_user.username} bienvenue sur THE-GEEK, votre adresse e-mail a été vérifiée avec succès."
        notification = Notification(user=my_user, message=message, is_read=False)
        notification.save()
        messages.add_message(request, messages.SUCCESS, "Votre adresse email a été vérifié avec succès.")
        return render(request, "all/sign_in.html", {"msg": messages.get_messages(request)})

    else:
        messages.add_message(request,messages.ERROR, 'votre vérifiction d\'adresse a échouer')
        return render(request,'all/index.html',{'msg':messages.get_messages(request)})
class Signin(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error':'les champs sont obligatoire'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            my_user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                firstname = user.first_name
                return Response({'msg': 'Connexion reuissie.'},status=status.HTTP_201_CREATED)

            elif my_user.is_active == False:
                return Response({'error':"Vous n'avez pas encore vérifier l'email"},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error':"L'authentification à échouer"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Erreur inconnue, reessayer.'},status=status.HTTP_400_BAD_REQUEST)



def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['mdp']
        if User.objects.filter(username=username):

            user = authenticate(username=username, password=password)
            my_user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                firstname = user.first_name
                return redirect('shop:index')
            elif my_user.is_active == False:
                messages.add_message(request, messages.WARNING,
                                         "Vous n'avez pas encore vérifier l'email")
                return render(request, "shop/sign_in.html", {"activate": messages.get_messages(request)})
            else:
                messages.add_message(request, messages.ERROR, "L'authentification à échouer")
                return render(request, "shop/sign_in.html", {"auth": messages.get_messages(request)})
        else:
            messages.add_message(request, messages.ERROR, "L'utilisateur n'existe pas")
            return render(request, "shop/sign_in.html", {"auth1": messages.get_messages(request)})

    return render(request, 'shop/sign_in.html')



# @login_required
def notification(request):

    notifications = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'notifications': notifications,
    }
    return render(request, 'all/notification.html', context)



@login_required
def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            firstname = request.POST['prenom']
            lastname = request.POST['nom']
            email = request.POST['email']
            password = request.POST['mdp']
            confirmpwd = request.POST['pwd']
            user = User.objects.get(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()
            if password == confirmpwd:
                user.password = password
                user.save()
            return redirect('profile')
        return render(request, 'all/profile.html')
    else:
        return redirect('connexion')
def log_out(request):
    logout(request)
    return redirect("all:index")
# erreur 404
def erreur_404(request,exception):
    return render(request,"all/404.html",status=404)
def email(request):
    return render(request, "all/email.html")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

