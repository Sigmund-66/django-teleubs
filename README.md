# TeleUBS 🏥

> Software de telessaúde para automatizar tarefas de rotina das Unidades Básicas de Saúde (UBS) no Brasil.

**Acesse em produção:** [django-teleubs.onrender.com](https://django-teleubs.onrender.com)

---

## 📋 Sobre o sistema

O **TeleUBS** é uma plataforma web de telessaúde desenvolvida para digitalizar e simplificar os processos das Unidades Básicas de Saúde (UBS). O sistema oferece dois portais distintos — um para **pacientes** e outro para **médicos** — permitindo o agendamento de consultas, solicitação de exames e gestão de prontuários de forma centralizada e acessível.

O projeto nasceu da necessidade de reduzir filas e processos manuais nas UBS, aproximando pacientes e profissionais de saúde por meio da tecnologia.

---

## 🛠️ Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| **Back-end** | Python 3 + Django 6 |
| **Banco de dados** | PostgreSQL (via Render) |
| **Servidor de produção** | Gunicorn |
| **Arquivos estáticos** | WhiteNoise |
| **Front-end** | HTML5, Bootstrap 5, Bootstrap Icons |
| **Autenticação** | Django Auth (senhas com hash PBKDF2) |
| **Variáveis de ambiente** | python-dotenv |
| **Deploy** | Render.com |

---

## 👤 Funcionalidades — Paciente

- **Cadastro:** Criação de conta com dados pessoais (CPF, RG, Cartão SUS, data de nascimento, nome dos pais, endereço e sexo)
- **Login / Logout:** Autenticação via CPF e senha
- **Agendamento de consulta:** Seleção de médico disponível, data e horário para marcação de consulta
- **Solicitação de exame:** Requisição de exames laboratoriais ou de imagem com data e horário preferidos
- **Prontuário:** Acesso ao histórico clínico pessoal, com visualização de todas as consultas e exames registrados

---

## 🩺 Funcionalidades — Médico

- **Cadastro:** Criação de conta profissional com CPF, CRM e especialidade médica
- **Login / Logout:** Acesso exclusivo pelo portal médico, com verificação de perfil profissional
- **Dashboard:** Painel com resumo das consultas agendadas, realizadas e total, além da agenda do dia
- **Agenda de consultas:** Listagem completa de todas as consultas vinculadas ao médico, ordenadas por data e horário

---

## 🚀 Rodando o projeto localmente

### Pré-requisitos

- Python 3.12 ou superior
- Git
- Um banco de dados PostgreSQL (local ou na nuvem) **ou** SQLite para testes rápidos

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/django-teleubs.git
cd django-teleubs
```

### 2. Criar e ativar o ambiente virtual

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar (Linux / macOS)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie o arquivo `.env` dentro da pasta `djangoproject/`:

```bash
cp djangoproject/.env.example djangoproject/.env  # se existir
# ou crie manualmente:
touch djangoproject/.env
```

Abra o `.env` e preencha com os seus dados:

```env
# Banco de dados PostgreSQL
DATABASE_HOSTNAME=localhost
DATABASE_NAME=teleubs
DATABASE_USER=seu_usuario
DATABASE_PORT=5432
DATABASE_PASSWORD=sua_senha

# Hosts permitidos
HOST_DEV1=127.0.0.1
HOST_DEV2=localhost
HOST_PRO=seu-dominio.onrender.com
```

> **Dica:** Para testes rápidos sem PostgreSQL, edite `djangoproject/mysite/settings.py` e descomente as linhas do SQLite:
> ```python
> 'ENGINE': 'django.db.backends.sqlite3',
> 'NAME': BASE_DIR / 'db.sqlite3',
> ```

### 5. Aplicar as migrações

```bash
cd djangoproject
python3 manage.py migrate
```

### 6. (Opcional) Criar um superusuário para o admin

```bash
python3 manage.py createsuperuser
```

### 7. Iniciar o servidor de desenvolvimento

```bash
python3 manage.py runserver
```

O sistema estará disponível em: **http://127.0.0.1:8000/**

### Rotas principais

| Rota | Descrição |
|---|---|
| `/` | Login do paciente |
| `/cadastro/` | Cadastro de paciente |
| `/home/` | Menu principal do paciente |
| `/agendar-consulta/` | Agendamento de consulta |
| `/solicitar-exame/` | Solicitação de exame |
| `/prontuario/` | Prontuário do paciente |
| `/medico/login/` | Login do médico |
| `/medico/cadastro/` | Cadastro de médico |
| `/medico/home/` | Dashboard do médico |
| `/admin/` | Painel administrativo Django |

---

## 📁 Estrutura do projeto

```
django-teleubs/
├── djangoproject/
│   ├── manage.py
│   ├── .env                  # Variáveis de ambiente (não versionado)
│   ├── mysite/               # Configurações do projeto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── teleubs/              # App principal
│       ├── models.py         # Paciente, Médico, Consulta, Exame, Prontuário
│       ├── views.py          # Lógica de negócio
│       ├── urls.py           # Rotas da aplicação
│       └── templates/ubs/    # Templates HTML
├── requirements.txt
├── build.sh                  # Script de build para o Render
└── README.md
```

---

## ☁️ Deploy no Render

O projeto está configurado para deploy na plataforma [Render.com](https://render.com). O arquivo `build.sh` na raiz do projeto executa automaticamente a instalação de dependências, coleta de arquivos estáticos e migrações a cada novo deploy.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.
