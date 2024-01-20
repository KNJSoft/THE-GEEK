from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

'''class Categorie(models.Model):
    nom=models.CharField(max_length=50)
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.nom

class Cour(models.Model):
    nom = models.CharField(max_length=80)
    description = models.TextField()
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.nom


class Lecon(models.Model):
    titre = models.CharField(max_length=100)
    texte = models.TextField()
    lien=models.URLField(max_length=256)
    texte_lien=models.CharField(max_length=64)
    cour = models.ForeignKey(Cour, on_delete=models.CASCADE)
    pdf_exists=models.BooleanField(default=False)
    pdf = models.ImageField(upload_to='pdfs/')
    imge_exists = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    video_exists = models.BooleanField(default=False)
    video = models.ImageField(upload_to='videos/')
    date = models.DateTimeField(auto_now_add=True)
    deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.titre'''

class Categorie(models.Model):
    titre=models.CharField(max_length=50)
    description=models.TextField()
    date_creation=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre
class Cours(models.Model):
    diff=(
        ('F','Facile'),
        ('M','Moyenne'),
        ('D','Difficile')
    )
    titre=models.CharField(max_length=200)
    description=models.TextField()
    categorie=models.ForeignKey(Categorie,on_delete=models.PROTECT)
    date_creation = models.DateTimeField(auto_now_add=True)
    instructeur=models.ForeignKey(User,on_delete=models.PROTECT)
    difficulte=models.CharField(max_length=1,choices=diff)
    duree_cours = models.TimeField()
    image_cours=models.ImageField(upload_to='media/images')
    prix=models.FloatField(default=0)
    def __str__(self):
        return self.titre
    class Meta:
        verbose_name_plural="Cours"

class Ressource(models.Model):
    types=(('PDF','fichiers pdf'),
           ('IMG','fichiers images'),
           ('MP4','fichiers video'),
           ('TXT','texte'),

        )

    titre=models.CharField(max_length=100)
    description=models.TextField()
    cours=models.ForeignKey(Cours,on_delete=models.PROTECT)
    type=models.CharField(max_length=3,choices=types)
    url_ressource=models.FileField(upload_to='media/ressources')
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre
class Progression(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT)
    cours=models.ForeignKey(Cours,on_delete=models.CASCADE)
    date_debut=models.DateTimeField(auto_now_add=True)
    date_fin=models.DateTimeField(auto_now_add=True)
    Score=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
class Badge(models.Model):
    nom=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='media/images')
    def __str__(self):
        return self.nom
    '''@property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url'''

class Competence(models.Model):
    badge=models.ForeignKey(Badge,on_delete=models.PROTECT)
    user=models.ForeignKey(User,on_delete=models.PROTECT)

class Quiz(models.Model):
    titre=models.CharField(max_length=50)
    cours=models.ForeignKey(Cours,on_delete=models.PROTECT)
    description=models.TextField()
    instructeur = models.ForeignKey(User, on_delete=models.PROTECT)
    date_creation=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre
class Question(models.Model):
    titre=models.TextField()
    quiz=models.ForeignKey(Quiz,on_delete=models.PROTECT)
    def __str__(self):
        return self.titre
class Choix(models.Model):
    question=models.ForeignKey(Question,on_delete=models.PROTECT)
    titre=models.TextField()
    def __str__(self):
        return self.titre
    class Meta:
        verbose_name_plural='Choix'

class Reponse(models.Model):
    question=models.ForeignKey(Question,on_delete=models.PROTECT)
    choix=models.ForeignKey(Choix,on_delete=models.PROTECT)
    correcte=models.BooleanField(default=True)
class ReponseUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT)
    question=models.ForeignKey(Question,on_delete=models.PROTECT)
    choix=models.ForeignKey(Choix,on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Reponse Utilisateur'
        verbose_name_plural = 'Reponses Utilisateurs'
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()


class MonModeleEmail(EmailMessage):
    def __init__(self, sujet, corps, destinataires):
        super().__init__(sujet, corps, 'knjprod@gmail.com', destinataires)
        self.content_subtype = 'html'
