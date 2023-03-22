from django.contrib import admin

# Register your models here.
from .models import *

class BranchesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Relations)
admin.site.register(Tag)
admin.site.register(Branch, BranchesAdmin)
admin.site.register(Language)
admin.site.register(User)