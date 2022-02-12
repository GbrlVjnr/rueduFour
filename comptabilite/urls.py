from django.urls import path

from . import views

urlpatterns = [
    path('<int:year>/', views.home, name='home'),
    path('import/', views.importBankData, name='importTransactions'),
]
