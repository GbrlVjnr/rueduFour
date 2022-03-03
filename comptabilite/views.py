# Navigation
from ast import Try
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# App configuration
from django.conf import settings
# Sum
from django.db.models import Sum


# Woob module (bank data retriever)
from woob.capabilities.bank.base import AccountNotFound

# App modules
from .models import Account, Distribution, Entry

# Python modules
from datetime import datetime, date

aujdh = datetime.now()

@login_required
def index(request):
    return redirect('home', year = aujdh.year)

def loginPage(request):

    context = {
        'title': "Connexion"
    }

    if request.method == "POST":

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'login.html', context)

def unlogUser(request):

    logout(request)

    return HttpResponseRedirect(settings.LOGIN_URL)

@login_required
def home(request, year):

    if request.method == "POST":

        entry = Entry.objects.get(pk=request.POST['entry_id'])

        if request.POST['form_type'] == "entry_edit":

            try:

                entry.label = request.POST['label']
                entry.VAT_rate = request.POST['VAT']
                entry.save()

                return redirect('home', aujdh.year)

            except:

                return redirect('home', aujdh.year)
        
        if request.POST['form_type'] == "distribution_edit":

            try:
                 # Distributes the transaction equally among tenants
                if request.POST['distribution'] == "tenants":
                    distributed_amount = entry.amount / 3
                    tenants = Account.objects.filter(contract="tenant")
                    for tenant in tenants:
                        if Distribution.objects.filter(entry=entry, account=tenant).exists():
                            Distribution.objects.filter(entry=entry, account=tenant).update(
                            entry=entry, account=tenant, amount=distributed_amount)
                        else:
                            new_distribution = Distribution(
                                entry=entry, account=tenant, amount=distributed_amount)
                            new_distribution.save()

                # Distributes the transaction among active accounts depending on their rent
                elif request.POST['distribution'] == "rent":
                    accounts = Account.objects.filter(is_active=True)
                    for account in accounts:
                        if account.contract == "tenant":
                            subrents_amount = accounts.aggregate(Sum('rent'))
                            if Distribution.objects.filter(entry=entry, account=account).exists():
                                Distribution.objects.filter(entry=entry, account=account).update(
                                    entry=entry, account=account, amount=distributed_amount)
                            else:
                                new_distribution = Distribution(
                                    entry=entry, account=account, amount=(entry.amount - subrents_amount['rent__sum'])/3)
                                new_distribution.save()
                        else:
                            if Distribution.objects.filter(entry=entry, account=account).exists():
                                Distribution.objects.filter(entry=entry, account=account).update(
                                    entry=entry, account=account, amount=distributed_amount)
                            else:
                                new_distribution = Distribution(
                                    entry=entry, account=account, amount=account.rent)
                                new_distribution.save()

                # Distributes the transaction depending on the amounts specified in the form
                elif request.POST['distribution'] == "custom":
                    for key, value in request.POST.items():
                        if key.startswith("account") and value != '':
                            if Distribution.objects.filter(entry=entry, account__id=int(key.split('_')[1])).exists():
                                account_to_assign = Account.objects.get(pk=int(key.split('_')[1]))
                                Distribution.objects.filter(entry=entry, account__id=int(key.split('_')[1])).update(
                                    entry=entry, account=account_to_assign, amount=float(value))
                            else:
                                print("new distribution")
                                account_to_assign = Account.objects.get(pk=int(key.split('_')[1]))
                                new_distribution = Distribution(
                                    entry=entry, account=account_to_assign, amount=float(value))
                                new_distribution.save()

                return redirect('home', aujdh.year)

            except:

                return redirect('home', aujdh.year)

    else:

        entries = Entry.objects.all().order_by('date')
        accounts = Account.objects.all().filter(is_active=True).order_by('full_name')

        allMonths = {
            1: 'janvier',
            2: 'février',
            3: 'mars',
            4: 'avril',
            5: 'mai',
            6: 'juin',
            7: 'juillet',
            8: 'août',
            9: 'septembre',
            10: 'octobre',
            11: 'novembre',
            12: 'décembre'
        }

        def monthly_total(type, year, month):
            amount = Entry.objects.filter(
                date__year=year,
                date__month=month,
                type=type).aggregate(Sum('amount'))['amount__sum']
            return amount

        incomeTotals = {}
        for key in allMonths.keys():
            incomeTotals[key] = monthly_total('INC', year, key)

        expenseTotals = {}
        for key in allMonths.keys():
            expenseTotals[key] = monthly_total('EXP', year, key)


        context = {
            'titre':  "ruedufourGestion",
            'page': "livre-journal",
            'year': year,
            'annee': allMonths,
            'aujdh': aujdh,
            'entrees': entries,
            'accounts': accounts,
            'incomeTotals': incomeTotals,
            'expenseTotals': expenseTotals,
        }
        return render(request, "livrejournal.html", context)
        
@login_required
def importBankData(request):
    from woob.core import Woob

    try:

        w = Woob()
        backend = w.build_backend('cragr', params={
            'website': settings.BANK_WEBSITE,
            'login': settings.BANK_LOGIN,
            'password': settings.BANK_PASSWORD,
        })

        bank_accounts = list(backend.iter_accounts())
        print(bank_accounts)
        all_transactions = backend.iter_history(bank_accounts[0])

        w.deinit()

        def databaseIsEmpty():
            if Entry.objects.all().exists():
                return False
            else:
                return True

        def isNew(transaction):
            if Entry.objects.filter(unique_id=transaction.unique_id()).exists():
                return False
            else:
                return True
            
        if databaseIsEmpty():
            transactions_to_import = all_transactions
        else :
            transactions_to_import = filter(isNew, all_transactions)

        transactions_counter = 0
        for transaction in transactions_to_import:
            if transaction.amount < 0:
                new_transaction = Entry(type='EXP', unique_id=transaction.unique_id(), date=transaction.date,
                                        label=transaction.label, amount=abs(transaction.amount))
            else:
                new_transaction = Entry(type='INC', unique_id=transaction.unique_id(),date=transaction.date,
                                        label=transaction.label, amount=abs(transaction.amount))
            new_transaction.save()
            transactions_counter += 1

        context = {
            'title': "Importation des données bancaires",
            'message': f"{transactions_counter} transaction(s) importée(s).",
            'transactions': transactions_to_import}

    except AccountNotFound:

        ErrorMessage = "Les données n'ont pas pu être chargées. Veuillez réessayer."
        context = {'errorMessage': ErrorMessage}

    return redirect('home', aujdh.year)

