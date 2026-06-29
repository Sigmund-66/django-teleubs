from django.urls import path
from . import views

urlpatterns = [
    # Áre do paciente
    path("", views.login_paciente, name="login_paciente"),
    path('home/', views.home, name='home'), # Tela menu do paciente
    path("telateste", views.telateste, name="telateste"),
    path('cadastro/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login/', views.login_paciente, name='login_paciente'),
    path('logout/', views.logout_paciente, name='logout_paciente'),
    path('agendar-consulta/', views.agendar_consulta, name='agendar_consulta'),
    path('solicitar-exame/', views.solicitar_exame, name='solicitar_exame'),
    path('prontuario/', views.acessar_prontuario, name='acessar_prontuario'),

    # Área do Médico
    path('medico/login/', views.login_medico, name='login_medico'),
    path('medico/logout/', views.logout_medico, name='logout_medico'),
    path('medico/cadastro/', views.cadastro_medico, name='cadastro_medico'),
    path('medico/home/', views.home_medico, name='home_medico'),
]