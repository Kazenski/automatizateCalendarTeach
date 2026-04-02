from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
import os

# Carrega as configurações do arquivo JSON
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    EMAIL_PROFESSOR = config.get("EMAIL_PROFESSOR", "")
    GRADE = config.get("GRADE", {})
except FileNotFoundError:
    print("Erro: O arquivo 'config.json' não foi encontrado na pasta do projeto.")
    exit()

MAPA_DIAS = {
    "segunda": "SEG", "terça": "TER", "quarta": "QUA", 
    "quinta": "QUI", "sexta": "SEX",
    "seg.": "SEG", "ter.": "TER", "qua.": "QUA", "qui.": "QUI", "sex.": "SEX"
}

def limpar_tela(driver):
    """Garante que as janelas de sucesso ou erro sejam fechadas."""
    for _ in range(3):
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.3)

def rodar_automacao():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao Chrome aberto...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception:
        print("ERRO: Chrome não encontrado na porta 9222. Siga as instruções do README.")
        return

    wait = WebDriverWait(driver, 8)
    slots_verificados = set()

    print("\nIniciando a varredura blindada...")

    while True:
        botoes = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'pm') or contains(@aria-label, 'am')]")
        botoes_visiveis = [b for b in botoes if b.is_displayed()]
        encontrou_novos_neste_ciclo = False
        
        for i in range(len(botoes_visiveis)):
            lista_atualizada = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'pm') or contains(@aria-label, 'am')]")
            visiveis_agora = [b for b in lista_atualizada if b.is_displayed()]
            
            if i >= len(visiveis_agora):
                break 
                
            botao = visiveis_agora[i]
            horario_botao = botao.get_attribute("aria-label").strip() 
            
            driver.execute_script("arguments[0].click();", botao)
            time.sleep(1.5) 
            
            try:
                dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
                texto_janela = dialog.text.lower()
                
                dia_detectado = next((sigla for nome, sigla in MAPA_DIAS.items() if nome in texto_janela), None)
                
                if not dia_detectado:
                    limpar_tela(driver)
                    continue
                
                chave_slot = f"{dia_detectado}-{horario_botao}"
                
                if chave_slot in slots_verificados:
                    limpar_tela(driver)
                    continue
                    
                slots_verificados.add(chave_slot)
                encontrou_novos_neste_ciclo = True
                
                if dia_detectado in GRADE and horario_botao in GRADE[dia_detectado]:
                    aula = GRADE[dia_detectado][horario_botao]
                    
                    # Logica flexível: se 'projeto' ou 'objetivo' não existirem no JSON, usa o nome da disciplina
                    texto_projeto = aula.get('projeto', aula['disc'])
                    texto_objetivo = aula.get('objetivo', aula['disc'])
                    
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
                        campos[5].send_keys(texto_projeto) # Injeta o Projeto
                        
                        campos[6].clear()
                        campos[6].send_keys(aula['alunos'])
                        
                        campos[7].clear()
                        campos[7].send_keys(texto_objetivo) # Injeta o Objetivo
                        
                        btn_reservar = dialog.find_element(By.XPATH, ".//button[span[text()='Reservar']]")
                        driver.execute_script("arguments[0].click();", btn_reservar)
                        
                        print("   SUCESSO! Aguardando 10 segundos de segurança...")
                        time.sleep(10)
                        limpar_tela(driver)
                        break 
                    else:
                        print("   [Erro] Formulário incompleto.")
                        limpar_tela(driver)
                else:
                    limpar_tela(driver)
                    
            except Exception as e:
                limpar_tela(driver)

        if not encontrou_novos_neste_ciclo:
            print("\n*** MAGNÍFICO! Varredura da semana concluída com sucesso. ***")
            break

if __name__ == "__main__":
    rodar_automacao()