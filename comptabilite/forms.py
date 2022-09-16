from django import forms
from .models import Account, Distribution, Entry, PrintsDistribution

class EditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        labels = {
            'label': 'Intitulé',
            'VAT_rate': 'Taux de la T.V.A.'
        }
        fields = ['unique_id','label', 'VAT_rate']
        widgets = {
            'unique_id': forms.HiddenInput(),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'VAT_rate': forms.Select(attrs={'class': 'form-control'}),
        }

class DistributionEditForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['account', 'amount']
        labels = {
            'account': 'Choisir un compte',
            'amount': 'Montant'
        }
        account = forms.ChoiceField(choices=Account.objects.all().values_list())
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
        }

class PrintDistributionForm(forms.ModelForm):
    class Meta:
        model = PrintsDistribution
        fields = ['account', 'type', 'amount']
        labels = {
            'account': 'Choisir un compte',
            'type': 'N&B ou Couleur',
            'amount': 'Quantité'
        }
        account = forms.ChoiceField(choices=Account.objects.all().values_list())
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'type': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }  