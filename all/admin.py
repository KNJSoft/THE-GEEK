from django.contrib import admin
from .models import *
# Register your models here.
class CategorieAdmin(admin.ModelAdmin):
    list_display=('nom','description','date','deleted')
    search_fields=['nom',]
class CourAdmin(admin.ModelAdmin):
    list_display=('nom','description','categorie','date','deleted')
    search_fields=['nom',]

class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre','lien','cour','pdf','image','video','date','deleted')
    search_fields = ['titre',]

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','message','is_read','created_at')
    search_fields = ['user',]



admin.site.register(Categorie,CategorieAdmin)
admin.site.register(Cour,CourAdmin)
admin.site.register(Lecon,LeconAdmin)
admin.site.register(Notification,NotificationAdmin)
#admin.site.register(MonModeleEmail)
ets="THE-GEEK"
admin.site.site_header=ets
admin.site.site_title=ets
admin.site.index_title=ets
