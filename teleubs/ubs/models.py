from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    # Relacionamento com o usuário base do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    cartaoSUS = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)

    def consultar_historico(self):
        pass

    def __str__(self):
        return self.usuario.get_full_name()

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    especialidade = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Dr(a). {self.usuario.get_full_name()} - {self.especialidade}"

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dataConsulta = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=50, default="Agendada")

    def agendar(self):
        self.status = "Agendada"
        self.save()

    def cancelar(self):
        self.status = "Cancelada"
        self.save()

class Exame(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    dataExame = models.DateField()
    resultado = models.TextField(blank=True, null=True)

    def solicitar(self):
        self.save()

class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    historicoClinico = models.TextField()

    def atualizar(self, novas_informacoes):
        self.historicoClinico += f"\n{novas_informacoes}"
        self.save()

# Create your models here.
