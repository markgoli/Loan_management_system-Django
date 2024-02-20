"""
URL configuration for core project.

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
from django.urls import path, include
from loan_products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # first page (Home page)
    path('register/', views.register, name='register'), # second page (Register page)
    path('login/', views.user_login, name='login'), # third page (Login page)
    path('logout/', views.user_logout, name='logout'), # url to view that logs out a user
    path('loan-products/', views.show, name='loan_products'), # forth page (View data from the db page)
    path('loan-products/new/', views.new_loan_product, name='new_loan_product'), # fifth page (Create new data page)
    path('loan-products/edit/<int:id>/', views.edit, name='edit_loan_product'), # six page (Update data page)
    path('loan-products/delete/<int:id>/', views.destroy, name='delete_loan_product'), # url to view that deletes an item
    path('set-session/', views.set_session_token, name='set_session_token'),
    path('session/', views.get_session_token, name='get_session_token'),
    path('members/', views.view_members, name='view_members'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #loan routes
    path('loans/', include('loans.urls')),
]
