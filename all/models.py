from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    nom=models.CharField(max_length=50)
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class Cour(models.Model):
    nom = models.CharField(max_length=80)
    description = models.TextField()
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)


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
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

