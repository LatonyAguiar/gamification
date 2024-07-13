from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChallengeForm, BrokerForm
from django.contrib.auth.decorators import login_required
from .models import Challenge, Broker, ChallengeAssignment
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm

@login_required
def home(request):
    return render(request, 'challenges/home.html')

@login_required
def create_challenge(request):
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
    challenge = get_object_or_404(Challenge, id=id)
    if request.method == 'POST':
        challenge.delete()
        messages.success(request, 'Desafio excluído com sucesso.')
        return redirect('list_challenges')
    return render(request, 'challenges/delet/delete_challenge.html', {'challenge': challenge})

@login_required
def assign_challenge(request):
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
    broker = get_object_or_404(Broker, id=broker_id)
    assigned_challenges = Challenge.objects.filter(challengeassignment__broker=broker)

    return render(request, 'challenges/view_assigned_challenges.html', {'broker': broker, 'assigned_challenges': assigned_challenges})

@login_required
def list_challenges(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/list/list_challenges.html', {'challenges': challenges})

@login_required
def challenge_details(request, id):
    return render(request, 'challenges/challenge_details.html')

@login_required
def accept_challenge(request, broker_id):
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

    # Renderize o template com o formulário de aceitação
    return render(request, 'challenges/accept_challenge.html', {'broker': broker})

@login_required
def create_broker(request):
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
    brokers = Broker.objects.all()

    for broker in brokers:
        assigned_challenges = Challenge.objects.filter(challengeassignment__broker=broker)
        broker.assigned_challenges = assigned_challenges

    return render(request, 'challenges/list/list_brokers.html', {'brokers': brokers})

@login_required
def edit_broker(request, id):
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
    broker = get_object_or_404(Broker, id=id)
    if request.method == 'POST':
        broker.delete()
        messages.success(request, 'Corretor excluído com sucesso.')
        return redirect('list_brokers')
    return render(request, 'challenges/delet/delete_broker.html', {'broker': broker})

@login_required
def create_user(request):
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
    users = User.objects.all()
    return render(request, 'challenges/list/list_users.html', {'users': users})

@login_required
def edit_user(request, id):
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
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso.')
        return redirect('list_users')
    return render(request, 'challenges/delet/delete_user.html', {'user': user})

@login_required
def accept_challenge(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)
    assigned_challenges = ChallengeAssignment.objects.filter(broker=broker, accepted=False)
    print('==>>> Broker:', broker)
    print('==>>> Broker ID:', broker_id)

    if request.method == 'POST':
        print('999', request.POST)  # Verifica se está recebendo os dados corretamente
        challenge_id = request.POST.get('challenge_id')
        action = request.POST.get('action')  # Captura o valor do botão pressionado
        print('ANTES')
        if challenge_id and action in ['accept', 'reject']:  # Verifica se o desafio ID e a ação são válidos
            try:
                print('Try-->')
                challenge = Challenge.objects.get(id=int(challenge_id))
                print('Try-->2')

                # Verifica se já existe uma atribuição desse desafio para esse corretor
                assignment = ChallengeAssignment.objects.filter(
                    challenge=challenge,
                    broker=broker
                ).first()
                if not assignment:
                    messages.error(request, 'Atribuição de desafio não encontrada.')
                    return redirect('list_brokers')

                print('Try-->3')
                if action == 'accept':
                    print('Aceitando desafio...')
                    assignment.accepted = True  # Marca o desafio como aceito
                    assignment.save()
                    print('Assignment salvo como aceito.')

                    # Marca o corretor como tendo desafio aceito
                    broker.accepted_challenge = True
                    broker.save()
                    print('Broker salvo com desafio aceito.')

                    messages.success(request, 'Você aceitou o desafio.')
                elif action == 'reject':
                    print('Rejeitando desafio...')
                    # Marca o corretor como não tendo desafio aceito
                    broker.accepted_challenge = False
                    broker.save()
                    print('Broker salvo com desafio rejeitado.')

                    messages.warning(request, 'Você rejeitou o desafio.')

                return redirect('list_brokers')

            except Challenge.DoesNotExist:
                messages.error(request, 'O desafio selecionado não existe.')
                print('Desafio não existe. Challenge ID:', challenge_id)

        else:
            messages.error(request, 'Ação inválida.')
            print('Ação inválida ou ID de desafio ausente. Challenge ID:', challenge_id, 'Action:', action)

        return redirect('list_brokers')

    context = {
        'broker': broker,
        'assigned_challenges': assigned_challenges,
    }
    return render(request, 'challenges/accept_challenge.html', context)



