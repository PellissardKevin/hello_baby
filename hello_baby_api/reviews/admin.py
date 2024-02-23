from django.contrib import admin
from .models import user, baby, forum, message, biberon, pregnancie, Image
from django.contrib.auth.models import Group


#admin.site.register(Product, ProductAdmin) <- admin.site.register method

admin.site.register(user)
admin.site.register(baby)
admin.site.register(pregnancie)
admin.site.register(forum)
admin.site.register(biberon)
admin.site.register(message)
admin.site.register(Image)


admin.site.site_header = "Product Review Admin"

