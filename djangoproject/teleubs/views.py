from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction
from datetime import date
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
        
        try:
            # Verificar se CPF já está cadastrado
            if User.objects.filter(username=cpf).exists():
                messages.error(request, 'Este CPF já está cadastrado.')
                return render(request, 'ubs/cadastro.html')
            
            with transaction.atomic():
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
                
        except DatabaseError as e:
            messages.error(request, 'Erro ao salvar os dados no banco de dados. Tente novamente.')
            return render(request, 'ubs/cadastro.html')
        except ValueError as e:
            messages.error(request, f'Dados inválidos: {e}')
            return render(request, 'ubs/cadastro.html')
        except Exception as e:
            messages.error(request, 'Ocorreu um erro inesperado. Tente novamente.')
            return render(request, 'ubs/cadastro.html')
        
        return redirect('home')
        
    return render(request, 'ubs/cadastro.html')

@login_required
def agendar_consulta(request):
    # Lógica para agendamento (EU2 - Agendar consulta) [cite: 22]
    try:
        medicos = Medico.objects.all()
    except DatabaseError:
        messages.error(request, 'Erro ao carregar a lista de médicos. Tente novamente.')
        return redirect('home')
    
    if request.method == "POST":
        medico_id = request.POST.get('medico_id')
        data_consulta = request.POST.get('data_consulta')
        horario = request.POST.get('horario')
        
        try:
            medico = Medico.objects.get(id=medico_id)
        except Medico.DoesNotExist:
            messages.error(request, 'Médico não encontrado. Por favor, selecione um médico válido.')
            return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})
        except DatabaseError:
            messages.error(request, 'Erro ao buscar informações do médico. Tente novamente.')
            return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})
        
        try:
            Consulta.objects.create(
                paciente=request.user.paciente,
                medico=medico,
                dataConsulta=data_consulta,
                horario=horario,
                status="Agendada"
            )
        except DatabaseError:
            messages.error(request, 'Erro ao agendar a consulta. Tente novamente.')
            return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})
        except Exception:
            messages.error(request, 'Ocorreu um erro inesperado ao agendar a consulta.')
            return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})
        
        return redirect('home')
        
    return render(request, 'ubs/agendar_consulta.html', {'medicos': medicos})

@login_required
def solicitar_exame(request):
    # Lógica para solicitação (EU5 - Solicitar exame) [cite: 23]
    if request.method == "POST":
        tipo = request.POST.get('tipo')
        data_exame = request.POST.get('data_exame')
        horario_exame = request.POST.get('horario_exame')
        
        try:
            Exame.objects.create(
                paciente=request.user.paciente,
                tipo=tipo,
                dataExame=data_exame,
                horarioExame=horario_exame,
                resultado="Pendente"
            )
        except DatabaseError:
            messages.error(request, 'Erro ao solicitar o exame. Tente novamente.')
            return render(request, 'ubs/solicitar_exame.html')
        except Exception:
            messages.error(request, 'Ocorreu um erro inesperado ao solicitar o exame.')
            return render(request, 'ubs/solicitar_exame.html')
        
        return redirect('home')
        
    return render(request, 'ubs/solicitar_exame.html')

@login_required
def acessar_prontuario(request):
    # Lógica para consultar histórico (EU3 - Acessar prontuário) [cite: 22]
    paciente = request.user.paciente
    
    try:
        consultas = Consulta.objects.filter(paciente=paciente)
        exames = Exame.objects.filter(paciente=paciente)
        prontuario, created = Prontuario.objects.get_or_create(
            paciente=paciente,
            defaults={'historicoClinico': 'Prontuário criado automaticamente.'}
        )
    except DatabaseError:
        messages.error(request, 'Erro ao carregar o prontuário. Tente novamente.')
        return redirect('home')
    except Exception:
        messages.error(request, 'Ocorreu um erro inesperado ao acessar o prontuário.')
        return redirect('home')
    
    context = {
        'consultas': consultas,
        'exames': exames,
        'prontuario': prontuario
    }
    return render(request, 'ubs/prontuario.html', context)


# ==================== ÁREA DO MÉDICO ====================

def login_medico(request):
    # Login exclusivo para médicos
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')

        user = authenticate(request, username=cpf, password=password)
        if user is not None:
            # Verifica se o usuário autenticado é um médico
            try:
                medico = user.medico
                login(request, user)
                return redirect('home_medico')
            except Medico.DoesNotExist:
                messages.error(request, 'Este usuário não tem perfil de médico.')
            except DatabaseError:
                messages.error(request, 'Erro ao verificar perfil. Tente novamente.')
        else:
            messages.error(request, 'CPF ou senha inválidos.')

    return render(request, 'ubs/login_medico.html')


def logout_medico(request):
    logout(request)
    return redirect('login_medico')


def cadastro_medico(request):
    # Cadastro de novo médico
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        crm = request.POST.get('crm')
        especialidade = request.POST.get('especialidade')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validar senhas
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'ubs/cadastro_medico.html')

        try:
            # Verificar se CPF já está cadastrado
            if User.objects.filter(username=cpf).exists():
                messages.error(request, 'Este CPF já está cadastrado.')
                return render(request, 'ubs/cadastro_medico.html')

            # Verificar se CRM já está cadastrado
            if Medico.objects.filter(crm=crm).exists():
                messages.error(request, 'Este CRM já está cadastrado.')
                return render(request, 'ubs/cadastro_medico.html')

            with transaction.atomic():
                # Cria o usuário Django
                usuario = User.objects.create_user(
                    username=cpf,
                    email=email,
                    password=password,
                    first_name=nome_completo
                )

                # Cria o médico
                Medico.objects.create(
                    usuario=usuario,
                    cpf=cpf,
                    crm=crm,
                    especialidade=especialidade
                )

        except DatabaseError:
            messages.error(request, 'Erro ao salvar os dados no banco de dados. Tente novamente.')
            return render(request, 'ubs/cadastro_medico.html')
        except ValueError as e:
            messages.error(request, f'Dados inválidos: {e}')
            return render(request, 'ubs/cadastro_medico.html')
        except Exception:
            messages.error(request, 'Ocorreu um erro inesperado. Tente novamente.')
            return render(request, 'ubs/cadastro_medico.html')

        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        return redirect('login_medico')

    return render(request, 'ubs/cadastro_medico.html')


@login_required(login_url='login_medico')
def home_medico(request):
    # Dashboard do médico — exibe dados e consultas vinculadas
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        messages.error(request, 'Perfil de médico não encontrado.')
        return redirect('login_medico')
    except DatabaseError:
        messages.error(request, 'Erro ao carregar perfil do médico. Tente novamente.')
        return redirect('login_medico')

    cpf = medico.cpf
    if len(cpf) == 11 and cpf.isdigit():
        cpf_mascarado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        cpf_mascarado = cpf

    try:
        consultas = Consulta.objects.filter(medico=medico).order_by('dataConsulta', 'horario')
        total_consultas = consultas.count()
        consultas_agendadas = consultas.filter(status='Agendada').count()
        consultas_realizadas = consultas.filter(status='Realizada').count()
    except DatabaseError:
        messages.error(request, 'Erro ao carregar as consultas. Tente novamente.')
        consultas = []
        total_consultas = 0
        consultas_agendadas = 0
        consultas_realizadas = 0
    except Exception:
        messages.error(request, 'Ocorreu um erro inesperado ao carregar as consultas.')
        consultas = []
        total_consultas = 0
        consultas_agendadas = 0
        consultas_realizadas = 0

    context = {
        'medico': medico,
        'cpf_mascarado': cpf_mascarado,
        'consultas': consultas,
        'total_consultas': total_consultas,
        'consultas_agendadas': consultas_agendadas,
        'consultas_realizadas': consultas_realizadas,
        'hoje': date.today().strftime('%d/%m/%Y'),
    }
    return render(request, 'ubs/home_medico.html', context)