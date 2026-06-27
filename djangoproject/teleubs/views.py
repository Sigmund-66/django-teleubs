from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Paciente, Consulta, Exame, Prontuario, Medico

# Create your views here.
def index(request):
    return HttpResponse('Hello, World. My first app using Django Framework')

def telateste(request):
    return HttpResponse('Welcome! How are you?')

def home(request):
    # Tela Menu do Paciente 
    if not request.user.is_authenticated:
        return redirect('login_paciente')
        
    cpf = request.user.paciente.cpf
    # CPF Masking (XXX.XXX.XXX-XX)
    if len(cpf) == 11 and cpf.isdigit():
        cpf_mascarado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        cpf_mascarado = cpf
        
    context = {
        'cpf_mascarado': cpf_mascarado
    }
    return render(request, 'ubs/home.html', context)

def login_paciente(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')
        
        user = authenticate(request, username=cpf, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'CPF ou senha inválidos.')
            
    return render(request, 'ubs/login.html')

def logout_paciente(request):
    logout(request)
    return redirect('login_paciente')

def cadastro_paciente(request):
    # Lógica de cadastro (EU1 - Cadastro de paciente) [cite: 22]
    if request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')
        cartao_sus = request.POST.get('cartao_sus')
        logradouro = request.POST.get('logradouro')
        
        # Cria o usuário Django
        usuario = User.objects.create_user(username=cpf, email=email, password=cpf, first_name=nome_completo)
        
        # Cria o paciente
        paciente = Paciente.objects.create(
            usuario=usuario,
            cpf=cpf,
            cartaoSUS=cartao_sus,
            telefone=telefone,
            endereco=logradouro
        )
        
        # Cria o prontuário do paciente recém-cadastrado
        Prontuario.objects.create(paciente=paciente, historicoClinico="Prontuário criado.")
        
        return redirect('home')
        
    return render(request, 'ubs/cadastro.html')

@login_required
def agendar_consulta(request):
    # Lógica para agendamento (EU2 - Agendar consulta) [cite: 22]
    medicos = Medico.objects.all()
    if request.method == "POST":
        medico_id = request.POST.get('medico_id')
        data_consulta = request.POST.get('data_consulta')
        horario = request.POST.get('horario')
        
        medico = Medico.objects.get(id=medico_id)
        
        Consulta.objects.create(
            paciente=request.user.paciente,
            medico=medico,
            dataConsulta=data_consulta,
            horario=horario,
            status="Agendada"
        )
        return redirect('home')
        
    return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})

@login_required
def solicitar_exame(request):
    # Lógica para solicitação (EU5 - Solicitar exame) [cite: 23]
    if request.method == "POST":
        tipo = request.POST.get('tipo')
        data_exame = request.POST.get('data_exame')
        
        Exame.objects.create(
            paciente=request.user.paciente,
            tipo=tipo,
            dataExame=data_exame,
            resultado="Pendente"
        )
        return redirect('home')
        
    return render(request, 'ubs/solicitar_exame.html')

@login_required
def acessar_prontuario(request):
    # Lógica para consultar histórico (EU3 - Acessar prontuário) [cite: 22]
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente)
    exames = Exame.objects.filter(paciente=paciente)
    prontuario = Prontuario.objects.get(paciente=paciente)
    
    context = {
        'consultas': consultas,
        'exames': exames,
        'prontuario': prontuario
    }
    return render(request, 'ubs/prontuario.html', context)