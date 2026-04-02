from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Configurações
EMAIL_PROFESSOR = "729145@profe.sed.sc.gov.br"

# Sua grade de aulas (os dias e horários exatos que você precisa)
GRADE = {
    "SEG": {
        "8:00pm": {"disc": "Modelagem de Sistemas/UML", "turma": "215-DS", "alunos": "25"},
        "8:40pm": {"disc": "Modelagem de Sistemas/UML", "turma": "215-DS", "alunos": "25"},
        "9:20pm": {"disc": "Práticas em Desenvolvimento de Sistemas I", "turma": "215-DS", "alunos": "25"},
    },
    "TER": {
        "7:00pm": {"disc": "Práticas em Desenvolvimento de Sistemas I", "turma": "215-DS", "alunos": "25"},
        "8:00pm": {"disc": "Práticas em Desenvolvimento de Sistemas I", "turma": "215-DS", "alunos": "25"},
        "8:40pm": {"disc": "Introdução a Banco de Dados", "turma": "112-DS", "alunos": "40"},
        "9:20pm": {"disc": "Introdução a Banco de Dados", "turma": "112-DS", "alunos": "40"},
    },
    "QUA": {
        "7:00pm": {"disc": "Introdução a Banco de Dados", "turma": "112-DS", "alunos": "40"},
        "8:00pm": {"disc": "Introdução à Programação", "turma": "112-DS", "alunos": "40"},
        "8:40pm": {"disc": "Introdução à Programação", "turma": "112-DS", "alunos": "40"},
    },
    "SEX": {
        "7:00pm": {"disc": "Linguagem SQL", "turma": "215-DS", "alunos": "25"},
        "8:00pm": {"disc": "Linguagem SQL", "turma": "215-DS", "alunos": "25"},
        "9:20pm": {"disc": "Introdução à Programação", "turma": "112-DS", "alunos": "40"},
    }
}

MAPA_DIAS = {
    "segunda": "SEG", "terça": "TER", "quarta": "QUA", 
    "quinta": "QUI", "sexta": "SEX",
    "seg.": "SEG", "ter.": "TER", "qua.": "QUA", "qui.": "QUI", "sex.": "SEX"
}

def limpar_tela(driver):
    """Metralhadora de ESC para garantir que as janelas de sucesso ou erro sejam fechadas."""
    for _ in range(3):
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.3)

def rodar_automacao():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao Chrome aberto...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 8)
    
    # Memória do robô (Ex: vai guardar "SEG-8:00pm", "TER-8:00pm")
    slots_verificados = set()

    print("\nIniciando a varredura blindada...")

    while True:
        # Pega todos os botões da tela
        botoes = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'pm') or contains(@aria-label, 'am')]")
        botoes_visiveis = [b for b in botoes if b.is_displayed()]
        
        encontrou_novos_neste_ciclo = False
        
        # Usamos o índice (i) para sempre pegar a lista mais fresca da tela
        for i in range(len(botoes_visiveis)):
            lista_atualizada = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'pm') or contains(@aria-label, 'am')]")
            visiveis_agora = [b for b in lista_atualizada if b.is_displayed()]
            
            if i >= len(visiveis_agora):
                break # A interface mudou (um agendamento sumiu), reinicia o processo
                
            botao = visiveis_agora[i]
            horario_botao = botao.get_attribute("aria-label").strip() # Pega apenas "8:00pm"
            
            driver.execute_script("arguments[0].click();", botao)
            time.sleep(1.5) # Aguarda a janela abrir
            
            try:
                # LÊ O QUE ESTÁ ESCRITO NA JANELA
                dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
                texto_janela = dialog.text.lower()
                
                dia_detectado = next((sigla for nome, sigla in MAPA_DIAS.items() if nome in texto_janela), None)
                
                if not dia_detectado:
                    limpar_tela(driver)
                    continue
                
                # Cria a chave única (ex: "TER-8:00pm")
                chave_slot = f"{dia_detectado}-{horario_botao}"
                
                # Se já olhamos ou agendamos essa chave específica, fecha e vai pro próximo
                if chave_slot in slots_verificados:
                    limpar_tela(driver)
                    continue
                    
                # Marca como verificado
                slots_verificados.add(chave_slot)
                encontrou_novos_neste_ciclo = True
                
                # É UM HORÁRIO DA SUA GRADE?
                if dia_detectado in GRADE and horario_botao in GRADE[dia_detectado]:
                    aula = GRADE[dia_detectado][horario_botao]
                    print(f"-> AULA ENCONTRADA: {dia_detectado} {horario_botao} ({aula['disc']})")
                    print("   Preenchendo...")
                    
                    campos = dialog.find_elements(By.XPATH, ".//input | .//textarea")
                    
                    if len(campos) >= 8:
                        campos[2].clear()
                        campos[2].send_keys(EMAIL_PROFESSOR)
                        campos[3].clear()
                        campos[3].send_keys(aula['disc'])
                        campos[4].clear()
                        campos[4].send_keys(aula['turma'])
                        campos[5].clear()
                        campos[5].send_keys(aula['disc'])
                        campos[6].clear()
                        campos[6].send_keys(aula['alunos'])
                        campos[7].clear()
                        campos[7].send_keys(aula['disc'])
                        
                        btn_reservar = dialog.find_element(By.XPATH, ".//button[span[text()='Reservar']]")
                        driver.execute_script("arguments[0].click();", btn_reservar)
                        
                        print("   SUCESSO! Aguardando 10 segundos de segurança...")
                        time.sleep(10)
                        limpar_tela(driver)
                        break # Quebra o FOR loop para recomeçar o WHILE (com a tela limpa e atualizada)
                    else:
                        print("   [Erro] Formulário incompleto.")
                        limpar_tela(driver)
                else:
                    # Não é da grade (ex: quinta-feira), apenas fecha e segue
                    limpar_tela(driver)
                    
            except Exception as e:
                # Se der qualquer engasgo de carregamento, limpa a tela e continua
                limpar_tela(driver)

        # Se ele verificou todos os botões visíveis e nenhum era "novo", ele acabou a semana.
        if not encontrou_novos_neste_ciclo:
            print("\n*** MAGNÍFICO! Varredura da semana concluída com sucesso. ***")
            break

if __name__ == "__main__":
    rodar_automacao()
