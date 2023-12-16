from django.contrib import admin

from noteally_app.models import Download, Like, Material, StudyArea, User

# Register your models here.

admin.site.register(Download)
admin.site.register(Like)
admin.site.register(Material)
admin.site.register(StudyArea)
admin.site.register(User)

