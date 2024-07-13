from django import forms
from .models import Challenge, Broker
from django.contrib.auth.models import User

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'banner', 'scoring_rules']

class BrokerForm(forms.ModelForm):
    username = forms.CharField(label='Nome de Usuário', required=False)
    cpf = forms.CharField(label='CPF')

    class Meta:
        model = Broker
        fields = ['username', 'cpf']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Digite o nome de usuário ou selecione abaixo'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        cpf = cleaned_data.get('cpf')

        if not username:
            raise forms.ValidationError('Você deve selecionar um usuário existente ou digitar um novo nome de usuário.')

        # Procurar o usuário pelo nome de usuário fornecido
        user = User.objects.filter(username=username).first()

        # Se o usuário não existir, criar um novo usuário
        if not user:
            user = User.objects.create_user(username=username)

        # Atualizar o objeto corretor com o usuário encontrado ou criado
        self.instance.user = user
        self.instance.cpf = cpf
        return cleaned_data
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }