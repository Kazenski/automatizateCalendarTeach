# 📅 automatizateCalendarTeach

Um bot em Python desenvolvido para automatizar o preenchimento maçante de reservas de aulas e laboratórios no Google Agenda (Google Appointments). Ideal para professores que precisam registrar dezenas de horários semanais com turmas, alunos, projetos e objetivos específicos.

---

## 🗂️ Estrutura do Projeto

O código foi pensado para separar completamente a lógica de programação dos dados das suas aulas. Assim, você só mexe na configuração!

```text
📦 automatizateCalendarTeach
 ┣ 📜 config.json          # Arquivo onde o usuário vai definir a grade e os textos das aulas
 ┣ 🐍 agendador.py         # O código em Python (Lógica principal e automação)
 ┣ 📋 requirements.txt     # Arquivo com as bibliotecas necessárias
 ┗ 📖 README.md            # Documentação do projeto para o GitHub
```

---

## 🚀 Como funciona?

O script se conecta a uma instância do Google Chrome já autenticada com a sua conta. Ele faz uma varredura visual no calendário da semana aberta, clica nos horários disponíveis, lê o dia da semana, cruza com a sua grade de horários configurada no arquivo JSON e injeta todos os dados no formulário automaticamente.

---

## 🛠️ Tecnologias

* **Python 3**
* **Selenium WebDriver**

---

## ⚙️ Como instalar e configurar

### 1. Clone o repositório
Abra o seu terminal e rode:
```bash
git clone [https://github.com/Kazenski/automatizateCalendarTeach.git](https://github.com/Kazenski/automatizateCalendarTeach.git)
cd automatizateCalendarTeach
```

### 2. Instale as dependências
Certifique-se de ter o Python instalado e instale o Selenium:
```bash
pip install -r requirements.txt
```

### 3. Configure a sua grade de aulas
Abra o arquivo `config.json` e insira as suas aulas da semana. 
* **`disc`**: Nome da disciplina.
* **`turma`**: Código da turma.
* **`alunos`**: Quantidade de alunos.
* **`projeto`**: (Opcional) Nome do projeto ou atividade do dia.
* **`objetivo`**: (Opcional) Objetivo de aprendizagem.

> 💡 *Dica: Se você omitir 'projeto' e 'objetivo', o script usará o nome da disciplina por padrão para evitar erros na hora do preenchimento.*

### 4. Inicie o Google Chrome em Modo de Depuração
Para que o bot consiga acessar sua conta sem ser bloqueado pelos sistemas de segurança do Google, precisamos abrir um Chrome especial com a porta de depuração habilitada.

Pressione `Windows + R` no seu teclado e cole o comando abaixo:
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeBotProfile"
```

Nesta nova janela que abrir:
1. Acesse o seu link de agendamento do Google Calendar.
2. Faça login na sua conta Google.
3. Posicione o calendário na semana exata que você deseja agendar (deixe na tela cheia).

### 5. Execute a Mágica!
Com a tela do calendário aberta e configurada, volte ao seu terminal ou VS Code e rode o script:
```bash
python agendador.py
```
Sente-se, pegue um café e veja o robô trabalhar por você. ☕

---

✍️ **Autor:** Professor Eduardo Kazenski  
Sinta-se livre para dar um ⭐ *Star*, fazer um *Fork* e contribuir com o projeto!
