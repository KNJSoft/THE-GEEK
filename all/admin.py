from django.contrib import admin
from .models import *
# Register your models here.
class CategorieAdmin(admin.ModelAdmin):
    list_display=('titre','description','date_creation')
    search_fields=['titre',]
class CoursAdmin(admin.ModelAdmin):
    list_display=('titre','description','categorie','date_creation','duree_cours','prix')
    search_fields=['titre',]

class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre','description','cours','type','url_ressource','date_creation',)
    search_fields = ['titre',]
class ProgressionAdmin(admin.ModelAdmin):
    list_display = ('user','cours','date_debut','date_fin','Score')
    search_fields = ['user',]

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('nom','description','image',)
    search_fields = ['nom',]

class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('user','badge',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre','cours','description','instructeur')
    search_fields = ['titre',]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('titre','quiz')
    search_fields = ['titre',]

class ChoixAdmin(admin.ModelAdmin):
    list_display = ('question','titre')

class ReponseAdmin(admin.ModelAdmin):
    list_display = ('question','choix','correcte')

class ReponseUserAdmin(admin.ModelAdmin):
    list_display = ('question','choix','user')
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','message','is_read','created_at')
    search_fields = ['user',]



admin.site.register(Categorie,CategorieAdmin)
admin.site.register(Cours,CoursAdmin)
admin.site.register(Ressource,RessourceAdmin)
admin.site.register(Progression,ProgressionAdmin)
admin.site.register(Badge,BadgeAdmin)
admin.site.register(Competence,CompetenceAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Reponse,ReponseAdmin)
admin.site.register(ReponseUser,ReponseUserAdmin)
admin.site.register(Choix,ChoixAdmin)
admin.site.register(Notification,NotificationAdmin)
#admin.site.register(MonModeleEmail)
ets="THE-GEEK"
admin.site.site_header=ets
admin.site.site_title=ets
admin.site.index_title=ets
