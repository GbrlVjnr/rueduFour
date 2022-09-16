from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.unlogUser, name="logout"),
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<int:year>/", views.home, name="home"),
    path("import/", views.importBankData, name="importTransactions"),
    path("facturation/<int:year>/<int:month>/", views.facturation, name="facturation"),
    path(
        "pdf_invoice/<int:year>/<int:month>/<int:accountid>/",
        views.pdf_invoice,
        name="pdf_invoice",
    ),
    path(
        "send_invoice/<int:year>/<int:month>/<int:accountid>/",
        views.send_invoice,
        name="send_invoice",
    ),
    path(
        "<int:year>/<int:month>/",
        login_required(views.EntriesMonthView.as_view(month_format="%m")),
        name="entry_month",
    ),
    path(
        "<int:year>/<str:month>/<int:day>/<int:pk>/",
        views.EntryDetailView.as_view(),
        name="entry_detail",
    ),
    path("edit-entry-form/<int:entry_id>/", views.edit_entry_form, name="edit-entry-form"),
    path("add-distribution-form/<int:entry_id>/", views.add_distribution_form, name="add-distribution-form"),
    path("distribute_auto/<str:type>/<int:entry_id>/", views.distribute_auto, name="distribute-auto"),
    path("delete_distribution/<int:distribution_id>/", views.delete_distrib, name="delete-distrib"),
    path("delete_printdistribution/<int:printdistribution_id>/", views.delete_printdistrib, name="delete-printdistrib"),
    path("reset_distrib/<int:entry_id>/", views.reset_distrib, name="reset-distrib"),
    path("add_printdistrib/<int:entry_id>/", views.add_printdistribution_form, name="add-printdistribution-form"),
]
