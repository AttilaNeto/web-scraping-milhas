from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
import time
import yaml

# CARREGAR ARQUIVO CONFIGURACAO
arquivo = open('config.yaml', 'r')
config = yaml.safe_load(arquivo)
hotmilhas = config['hotmilhas']

# DADOS PARA LOGAR NO SITE DA HOTMILHAS
email = hotmilhas['email']
senha = hotmilhas['senha']

# INFORMACOES PARA O NAVEGADOR
linkHotmilhas = 'https://cliente.hotmilhas.com.br/app/quotation'
linkMaxMilhas = 'https://www.maxmilhas.com.br/vender-milhas'
options = Options()
options.headless = False  # true = não exibe a tela / false = exibe a tela
navegador = webdriver.Firefox(options=options)
navegador.maximize_window()  # maximiza a tela para entrar

# variaveis
site = 0
primeiroAcesso = True

def EntrarSiteHotmilhas():
    navegador.get(url=linkHotmilhas)
    sleep(5)
    navegador.find_element(by=By.NAME, value='email').send_keys(email)
    sleep(1)
    navegador.find_element(by=By.NAME, value='password').send_keys(senha)
    sleep(1)
    navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[2]/div/div/div[2]/div[1]/form/div[2]/div[4]/button/div').click()
    sleep(8)
    navegador.find_element(by=By.CSS_SELECTOR, value='.la2BYY.la22Uy.la3ZgL.la1bmA').click()
    sleep(2)
    return

def RealizarCotacaoHotmilhas(): 
    navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/button/div[1]').click()
    sleep(3)
    # condição feita porque a class muda de nome a cada clique
    sleep(1)
    navegador.find_element(by=By.XPATH, value='//*[@id="react-select-4-input"]').send_keys('smiles' + Keys.ENTER)
    sleep(2)
    DigitarMilhas(1)
    sleep(2)
    navegador.find_element(by=By.XPATH, value='//*[@id="react-select-72-input"]').send_keys('latam' + Keys.ENTER)
    sleep(2)
    DigitarMilhas(2)
    sleep(2)
    navegador.find_element(by=By.XPATH, value='//*[@id="react-select-140-input"]').send_keys('tudo azul' + Keys.ENTER)
    sleep(2)
    DigitarMilhas(3)
    sleep(4)
    return

def PegarValores(totalMilhas,idPrograma):
    ListaMilhas = []
    programa = idPrograma
    sleep(5)
    dia01 = RemoverCaracter(navegador.find_element(
        by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[1]/div').text, totalMilhas)
    ListaMilhas.append(dia01)
    dia30 = RemoverCaracter(navegador.find_element(
        by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[2]/div').text, totalMilhas)
    ListaMilhas.append(dia30)
    dia45 = RemoverCaracter(navegador.find_element(
        by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[3]/div').text, totalMilhas)
    ListaMilhas.append(dia45)
    dia60 = RemoverCaracter(navegador.find_element(
        by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[4]/div').text, totalMilhas)
    ListaMilhas.append(dia60)
    sleep(1)
    AtualizarMilhasHotmilhas(ListaMilhas, totalMilhas, programa)
    return

def DigitarMilhas(idPrograma):
    milhas = [20,30,50,70,100]
    for i in range (0,5):
        milhaponto = (str(milhas[i])+".")
        navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys(milhaponto+Keys.ENTER)
        sleep(2)
        PegarValores(milhas[i],idPrograma)
        i += 1

def RemoverCaracter(palavra, milha):
    caracter = "R$ ."
    for x in range(len(caracter)):
        palavra = palavra.replace(caracter[x], "")
    palavra = palavra.replace(",", ".")
    palavra = (float(palavra)/int(milha))
    return (palavra)

def AtualizarMilhasHotmilhas(listaDia, totalMilhas, idPrograma):
    conn = sqlite3.connect(
        "D:\#PROJETOS\BOT-TELEGRAM-MILHAS\database\database.db")
    cursor = conn.cursor()
    sql = ("""UPDATE DIAS_VALORES SET DIA01=?,DIA30=?,DIA45=?,DIA60=? WHERE IDMILHAS = (select idMilhas from milhas where TotalMilhas = ? and idPrograma = ?)""")
    cursor.execute(sql,(listaDia[0], listaDia[1],listaDia[2], listaDia[3], totalMilhas, idPrograma))
    conn.commit()
    conn.close()
    return

def CotacaoHotmilhas():
    global primeiroAcesso
    if primeiroAcesso == True:
        EntrarSiteHotmilhas()
        primeiroAcesso = False
    else:
        navegador.get(url=linkHotmilhas)
        sleep(5)
    RealizarCotacaoHotmilhas()


def CotacaoMaxMilhas():
    navegador.get(url=linkMaxMilhas)
    sleep(4)

def Cotacao():
    global site
    while site < 2:
        if site == 0:
            CotacaoHotmilhas()
            site = 1
        else:
            CotacaoMaxMilhas()
            site = 0


def main():
    Cotacao()

if __name__ == '__main__':
    main()