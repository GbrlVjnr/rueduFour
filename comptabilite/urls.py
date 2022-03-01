from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.unlogUser, name='logout'),
    path('', views.index, name='index'),
    path('<int:year>/', views.home, name='home'),
    path('import/', views.importBankData, name='importTransactions'),
]
