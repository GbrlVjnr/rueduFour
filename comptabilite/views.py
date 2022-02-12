from django.shortcuts import render, redirect

from woob.capabilities.bank.base import AccountNotFound

from .models import Account, Distribution, Entry

from datetime import datetime, date

aujdh = datetime.now().date

def home(request, year):

    entries = Entry.objects.all().order_by('date')

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

    context = {
        'titre':  "rueduFour",
        'page': "livre-journal",
        'year': year,
        'annee': allMonths,
        'aujdh': aujdh,
        'entrees': entries,
    }
    return render(request, "livrejournal.html", context)

def importBankData(request):
    from woob.core import Woob
    from woob.capabilities.bank import CapBank

    try:

        w = Woob()
        w.load_backends(CapBank)

        bank_accounts = list(w.iter_accounts())
        all_transactions = w.iter_history(bank_accounts[0])

        def databaseIsEmpty():
            if Entry.objects.all().exists():
                return False
            else:
                return True

        def isNew(transaction):
            last_entry = Entry.objects.latest('date')

            if transaction.date >= last_entry.date and abs(transaction.amount) != last_entry.amount:
                return True
            else:
                return False
            
        if databaseIsEmpty():
            transactions_to_import = all_transactions
        else :
            transactions_to_import = filter(isNew, all_transactions)

        transactions_counter = 0
        for transaction in transactions_to_import:
            if transaction.amount < 0:
                new_transaction = Entry(type='EXP', date=transaction.date,
                                        label=transaction.label, amount=abs(transaction.amount))
            else:
                new_transaction = Entry(type='INC', date=transaction.date,
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

    return redirect('home', aujdh.year, context)

