from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('user/', views.userPage, name='user'),
    path('account/', views.accountSettings, name='account'),

    path('products/', views.products, name='products'),
    path('customer/<int:id>', views.customer, name='customer'),
    
    path('create_order/<int:id>', views.createOrder, name='createOrder'),
    path('update_order/<int:id>', views.updateOrder, name='updateOrder'),
    path('delete_order/<int:id>', views.deleteOrder, name='deleteOrder'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),

]