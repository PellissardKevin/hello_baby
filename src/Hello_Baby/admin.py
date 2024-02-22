from django.contrib import admin
from .models import Account
from .models import User

admin.site.register(Account)
admin.site.register(User)
