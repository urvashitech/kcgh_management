from django import forms
from .models import Profile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'sch_no': forms.NumberInput(attrs={'class': 'form-input'}),
            'branch': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'category': forms.TextInput(attrs={'class': 'form-input'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.NumberInput(attrs={'class': 'form-input'}),
            'g_no': forms.NumberInput(attrs={'class': 'form-input'}),
            'g_name': forms.TextInput(attrs={'class': 'form-input'}),
            'g_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'g_occupation': forms.TextInput(attrs={'class': 'form-input'}),
            'g_address': forms.TextInput(attrs={'class': 'form-input'}),
            'e_no': forms.NumberInput(attrs={'class': 'form-input'}),
            'l_name': forms.TextInput(attrs={'class': 'form-input'}),
            'l_address': forms.TextInput(attrs={'class': 'form-input'}),
            'l_no': forms.NumberInput(attrs={'class': 'form-input'}),
            'disease': forms.TextInput(attrs={'class': 'form-input'}),
        }
