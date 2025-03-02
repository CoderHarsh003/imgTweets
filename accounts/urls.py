from django.urls import path
from . import views

urlpatterns = [
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('upload/', views.upload_image, name='upload_image'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]