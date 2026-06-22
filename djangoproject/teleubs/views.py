from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Paciente, Consulta, Exame, Prontuario, Medico

# Create your views here.
def index(request):
    return HttpResponse('Hello, World. My first app using Django Framework')

def telateste(request):
    return HttpResponse('Welcome! How are you?')

def home(request):
    # Tela Menu do Paciente 
    return render(request, 'ubs/home.html')

def cadastro_paciente(request):
    # Lógica de cadastro (EU1 - Cadastro de paciente) [cite: 22]
    if request.method == "POST":
        # Processamento do formulário HTML seria inserido aqui
        pass
    return render(request, 'ubs/cadastro.html')

@login_required
def agendar_consulta(request):
    # Lógica para agendamento (EU2 - Agendar consulta) [cite: 22]
    medicos = Medico.objects.all()
    if request.method == "POST":
        # Capturar dados do form e instanciar nova Consulta
        pass
    return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})

@login_required
def solicitar_exame(request):
    # Lógica para solicitação (EU5 - Solicitar exame) [cite: 23]
    if request.method == "POST":
        # Capturar dados do form e instanciar novo Exame
        pass
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