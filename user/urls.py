from django.urls import path, include
from . import views


app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('account/details/', views.UserDetailsView.as_view(), name='user-details-and-update'), # can use GET and PATCH requests
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
    path('account/delete/', views.DeleteAccountView.as_view(), name='delete-account'),
]
