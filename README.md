# 📅 automatizateCalendarTeach

Um bot em Python desenvolvido para automatizar o preenchimento maçante de reservas de aulas e laboratórios no Google Agenda (Google Appointments). Ideal para professores que precisam registrar dezenas de horários semanais com turmas, alunos, projetos e objetivos específicos.

## 🗂️ Estrutura do Projeto

automatizateCalendarTeach/
│
├── config.json          # Arquivo onde o usuário vai definir a grade e os textos
├── agendador.py         # O código em Python (Lógica principal)
├── requirements.txt     # Arquivo com as bibliotecas necessárias
└── README.md            # Documentação do projeto para o GitHub


## 🚀 Como funciona?
O script se conecta a uma instância do Google Chrome já autenticada com a sua conta. Ele faz uma varredura visual no calendário da semana aberta, clica nos horários disponíveis, lê o dia da semana, cruza com a sua grade de horários configurada no arquivo JSON e injeta todos os dados no formulário automaticamente.

## 🛠️ Tecnologias
* Python 3
* Selenium WebDriver

## ⚙️ Como instalar e configurar

### 1. Clone o repositório
\`\`\`bash
git clone https://github.com/Kazenski/automatizateCalendarTeach.git
cd automatizateCalendarTeach
\`\`\`

### 2. Instale as dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure a sua grade de aulas
Abra o arquivo `config.json` e insira as suas aulas. 
* **disc:** Nome da disciplina.
* **turma:** Código da turma.
* **alunos:** Quantidade de alunos.
* **projeto:** (Opcional) Nome do projeto ou atividade do dia.
* **objetivo:** (Opcional) Objetivo de aprendizagem.
*(Se você omitir 'projeto' e 'objetivo', o script usará o nome da disciplina por padrão).*

### 4. Inicie o Google Chrome em Modo de Depuração
Para que o bot consiga acessar sua conta sem ser bloqueado pelos sistemas de segurança do Google, precisamos abrir um Chrome especial com a porta de depuração habilitada.

Pressione `Windows + R` no seu teclado e cole o comando abaixo:
\`\`\`cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeBotProfile"
\`\`\`

Nesta janela que abrir:
1. Acesse o seu link de agendamento do Google Calendar.
2. Faça login na sua conta Google.
3. Posicione o calendário na semana que deseja agendar.

### 5. Execute a Mágica!
Com a tela do calendário aberta e configurada, rode o script:
\`\`\`bash
python agendador.py
\`\`\`
Sente-se, pegue um café e veja o robô trabalhar por você. ☕

---
**Autor:** Professor Eduardo Kazenski  
Sinta-se livre para dar um *Fork* e contribuir com o projeto!
