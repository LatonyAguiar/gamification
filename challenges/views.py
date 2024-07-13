from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChallengeForm, BrokerForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Challenge, Broker, ChallengeAssignment
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def home(request):
    """Renderiza a página inicial."""
    return render(request, 'challenges/home.html')

@login_required
def create_challenge(request):
    """Cria um novo desafio."""
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_challenges')  # Redireciona para a lista de desafios após salvar
    else:
        form = ChallengeForm()
    return render(request, 'challenges/create/create_challenge.html', {'form': form})

@login_required
def edit_challenge(request, id):
    """Edita um desafio existente."""
    challenge = get_object_or_404(Challenge, id=id)
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Desafio atualizado com sucesso.')
            return redirect('list_challenges')
    else:
        form = ChallengeForm(instance=challenge)
    return render(request, 'challenges/edit/edit_challenge.html', {'form': form})

@login_required
def delete_challenge(request, id):
    """Exclui um desafio."""
    challenge = get_object_or_404(Challenge, id=id)
    if request.method == 'POST':
        challenge.delete()
        messages.success(request, 'Desafio excluído com sucesso.')
        return redirect('list_challenges')
    return render(request, 'challenges/delet/delete_challenge.html', {'challenge': challenge})

@login_required
def assign_challenge(request):
    """Atribui um desafio a um corretor."""
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge')
        broker_cpf = request.POST.get('broker_cpf')

        challenge = Challenge.objects.get(id=challenge_id)
        broker = Broker.objects.get(cpf=broker_cpf)

        assignment, created = ChallengeAssignment.objects.get_or_create(
            challenge=challenge,
            broker=broker
        )

        if created:
            messages.success(request, 'Desafio atribuído com sucesso.')
        else:
            messages.warning(request, 'Este desafio já foi atribuído a este corretor.')

        return redirect('list_brokers')

    challenges = Challenge.objects.all()
    brokers = Broker.objects.all()
    return render(request, 'challenges/assign_challenge.html', {'challenges': challenges, 'brokers': brokers})

@login_required
def view_assigned_challenges(request, broker_id):
    """Exibe os desafios atribuídos a um corretor específico."""
    broker = get_object_or_404(Broker, id=broker_id)
    assigned_challenges = Challenge.objects.filter(challengeassignment__broker=broker)

    return render(request, 'challenges/view_assigned_challenges.html', {'broker': broker, 'assigned_challenges': assigned_challenges})

@login_required
def list_challenges(request):
    """Lista todos os desafios."""
    challenges = Challenge.objects.all()
    return render(request, 'challenges/list/list_challenges.html', {'challenges': challenges})

@login_required
def accept_challenge(request, broker_id):
    """Aceita ou rejeita um desafio por parte de um corretor."""
    broker = get_object_or_404(Broker, id=broker_id)
    
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge_id')
        if challenge_id:
            try:
                challenge = Challenge.objects.get(id=int(challenge_id))
                
                # Verifica se já existe uma atribuição desse desafio para esse corretor
                assignment, created = ChallengeAssignment.objects.get_or_create(
                    challenge=challenge,
                    broker=broker
                )

                if created:
                    messages.success(request, 'Você aceitou participar do desafio.')
                else:
                    messages.warning(request, 'Este desafio já foi aceito anteriormente.')

                return redirect('list_brokers')  # Redireciona para a lista de corretores após aceitar o desafio
            except Challenge.DoesNotExist:
                messages.error(request, 'O desafio selecionado não existe.')
        else:
            messages.error(request, 'ID do desafio não foi fornecido.')

    # Renderiza o template com o formulário de aceitação
    return render(request, 'challenges/accept_challenge.html', {'broker': broker})

@login_required
def create_broker(request):
    """Cria um novo corretor."""
    if request.method == 'POST':
        form = BrokerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Corretor cadastrado com sucesso.')
            return redirect('list_brokers')
    else:
        form = BrokerForm()
    return render(request, 'challenges/create/create_broker.html', {'form': form})

@login_required
def list_brokers(request):
    """Lista todos os corretores e seus desafios atribuídos."""
    brokers = Broker.objects.all()

    for broker in brokers:
        assigned_challenges = Challenge.objects.filter(challengeassignment__broker=broker)
        broker.assigned_challenges = assigned_challenges

    return render(request, 'challenges/list/list_brokers.html', {'brokers': brokers})

@login_required
def edit_broker(request, id):
    """Edita um corretor existente."""
    broker = get_object_or_404(Broker, id=id)
    if request.method == 'POST':
        form = BrokerForm(request.POST, instance=broker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Corretor atualizado com sucesso.')
            return redirect('list_brokers')
    else:
        form = BrokerForm(instance=broker)
    return render(request, 'challenges/edit/edit_broker.html', {'form': form})

@login_required
def delete_broker(request, id):
    """Exclui um corretor."""
    broker = get_object_or_404(Broker, id=id)
    if request.method == 'POST':
        broker.delete()
        messages.success(request, 'Corretor excluído com sucesso.')
        return redirect('list_brokers')
    return render(request, 'challenges/delet/delete_broker.html', {'broker': broker})

@login_required
def create_user(request):
    """Cria um novo usuário."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            # Você pode adicionar outras lógicas relacionadas ao Broker aqui, se necessário
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('list_users')  # Redireciona para a lista de usuários após salvar
    else:
        form = UserForm()
    return render(request, 'challenges/create/create_user.html', {'form': form})

@login_required
def list_users(request):
    """Lista todos os usuários."""
    users = User.objects.all()
    return render(request, 'challenges/list/list_users.html', {'users': users})

@login_required
def edit_user(request, id):
    """Edita um usuário existente."""
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('list_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'challenges/edit/edit_user.html', {'form': form})

@login_required
def delete_user(request, id):
    """Exclui um usuário."""
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso.')
        return redirect('list_users')
    return render(request, 'challenges/delet/delete_user.html', {'user': user})
