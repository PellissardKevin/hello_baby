"""
URL configuration for hello_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hello_baby import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='Login'), name='login'),
    path('user/', views.user_list, name='user_list'),
    path('user/<int:id>', views.user_details),
    path('user/baby/<int:id_user>', views.BabyUser.as_view()),
    path('baby/<int:id>', views.baby_details),
    path('forums/', views.forum_list),
    path('forums/<int:id}', views.forum_details),
    path('forums/<int:id_user>', views.ForumUser.as_view()),
    path('forums/<int:forum_id>/messages/', views.forum_message_list),
    path('forums/<int:forum_id>/messages/<int:message_id>', views.forum_message_details),
]
