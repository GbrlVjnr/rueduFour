from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.unlogUser, name='logout'),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:year>/', views.home, name='home'),
    path('import/', views.importBankData, name='importTransactions'),
    path('facturation/<int:year>/<int:month>/', views.facturation, name='facturation'),
    path('pdf_invoice/<int:year>/<int:month>/<int:accountid>/', views.pdf_invoice, name='pdf_invoice'),
    path('send_invoice/<int:year>/<int:month>/<int:accountid>/', views.send_invoice, name='send_invoice'),
]
