from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html',success_url = '/'), name='change_password'),
    path('userdata/', views.UserDataList.as_view(), name='userdata'),
    path('userdata/<int:pk>/', views.SingleUserDataList.as_view()),
    path('employment/', views.Employments.as_view(), name='employment'),
    path('employment/<int:pk>/', views.Employments.as_view(), name='employment'),
    path('hobbies/', views.Hobbies.as_view(), name='hobbies'),
]