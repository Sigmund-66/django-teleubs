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
    # Lógica de cadastro (EU1 - Cadastro de paciente) 
    if request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        cartao_sus = request.POST.get('cartao_sus')
        logradouro = request.POST.get('logradouro')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        nome_mae = request.POST.get('nome_mae')
        nome_pai = request.POST.get('nome_pai')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validar senhas
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'ubs/cadastro.html')
            
        # Verificar se CPF já está cadastrado
        if User.objects.filter(username=cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado.')
            return render(request, 'ubs/cadastro.html')
            
        # Cria o usuário Django (o método create_user criptografa a senha automaticamente usando hash seguro/PBKDF2)
        usuario = User.objects.create_user(username=cpf, email=email, password=password, first_name=nome_completo)
        
        # Cria o paciente
        paciente = Paciente.objects.create(
            usuario=usuario,
            cpf=cpf,
            cartaoSUS=cartao_sus,
            telefone=telefone,
            endereco=logradouro,
            RG=int(rg) if rg else 0,
            dataNascimento=data_nascimento if data_nascimento else None,
            sexo=sexo if sexo else "",
            nomeMae=nome_mae if nome_mae else "",
            nomePai=nome_pai if nome_pai else ""
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
        horario_exame = request.POST.get('horario_exame')
        
        Exame.objects.create(
            paciente=request.user.paciente,
            tipo=tipo,
            dataExame=data_exame,
            horarioExame=horario_exame,
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
    prontuario, created = Prontuario.objects.get_or_create(
        paciente=paciente,
        defaults={'historicoClinico': 'Prontuário criado automaticamente.'}
    )
    
    context = {
        'consultas': consultas,
        'exames': exames,
        'prontuario': prontuario
    }
    return render(request, 'ubs/prontuario.html', context)