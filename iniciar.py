from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import sqlite3
import schedule
import time
import yaml


# CARREGAR ARQUIVO CONFIGURACAO
arquivo = open('config.yaml', 'r')
config = yaml.safe_load(arquivo)
hotmilhas = config['hotmilhas']
banco = config['banco']

# DADOS PARA LOGAR NO SITE DA HOTMILHAS
email = hotmilhas['email']
senha = hotmilhas['senha']

options1 = Options()
options1.headless = False
navegador = webdriver.Firefox(options=options1)
link = 'https://cliente.hotmilhas.com.br/app/quotation'
acesso = 1

def AtualizarValores(listaDia,totalMilhas,idPrograma):
    global banco
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    sql = ("""UPDATE DIAS_VALORES SET DIA01=?,DIA30=?,DIA45=?,DIA60=? WHERE IDMILHAS = (select idMilhas from milhas where TotalMilhas = ? and idPrograma = ?)""")
    cursor.execute(sql,(listaDia[0],listaDia[1],listaDia[2],listaDia[3],totalMilhas,idPrograma))
    conn.commit()
    conn.close()
    return
    
def LogarSite():
    navegador.get(url=link)
    navegador.maximize_window()
    sleep(5)
    navegador.find_element(by=By.NAME, value='email').send_keys(email)
    sleep(1)
    navegador.find_element(by=By.NAME, value='password').send_keys(senha)
    sleep(1)
    navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[2]/div/div/div[2]/div[1]/form/div[2]/div[4]/button/div').click()
    sleep(8)
    navegador.find_element(by=By.CSS_SELECTOR, value='.la2BYY.la22Uy.la3ZgL.la1bmA').click()
    sleep(2)
    navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/button/div[1]').click()
    sleep(1)
    return

def RealizarCotacao(programa,idPrograma):
    global acesso

    print(programa)
    if (acesso==1):
        navegador.find_element(by=By.XPATH, value='//*[@id="react-select-4-input"]').send_keys(programa + Keys.ENTER)
    elif acesso==2:
        navegador.find_element(by=By.XPATH, value='//*[@id="react-select-76-input"]').send_keys(programa + Keys.ENTER)
    else: 
        navegador.find_element(by=By.XPATH, value='//*[@id="react-select-148-input"]').send_keys(programa + Keys.ENTER)


    sleep(4)
    navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys('20.'+Keys.ENTER)
    sleep(2)
    PegarValores(20,idPrograma)
    navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys('30.'+Keys.ENTER)
    PegarValores(30,idPrograma)
    sleep(2)
    navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys('50.'+Keys.ENTER)
    PegarValores(50,idPrograma)
    sleep(2)
    navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys('70.'+Keys.ENTER)
    PegarValores(70,idPrograma)
    sleep(2)
    navegador.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div/input').send_keys('100.'+Keys.ENTER)
    PegarValores(100,idPrograma)
    sleep(2)
    navegador.find_element(by=By.XPATH, value="/html/body/div[3]/div/div[3]/div[2]/div/div/div/div[2]/header/button").click()
    sleep(2)
    return

def NovaCotacao():
    navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/button/div[1]').click()
    sleep(1)
    return
    
def PegarValores(totalMilhas,Idprograma):
    ListaMilhas =[]
    programa = Idprograma
    sleep(5)
    dia01 = RemoverCaracter(navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[1]/div').text,totalMilhas)
    ListaMilhas.append(dia01)
    dia30 = RemoverCaracter(navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[2]/div').text,totalMilhas)
    ListaMilhas.append(dia30)
    dia45 = RemoverCaracter(navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[3]/div').text,totalMilhas)
    ListaMilhas.append(dia45)
    dia60 = RemoverCaracter(navegador.find_element(by=By.XPATH, value='//*[@id="*"]/div/div[3]/div[2]/div/div/div/div[2]/main/div/div[2]/ul/li[4]/div').text,totalMilhas)
    ListaMilhas.append(dia60)
    sleep(1)
    AtualizarValores(ListaMilhas,totalMilhas,programa)


    return

def RemoverCaracter(palavra,milha):
    caracter = "R$ ."
    for x in range(len(caracter)):
        palavra = palavra.replace(caracter[x],"")
    
    palavra = palavra.replace(",",".")
    
    palavra = (float(palavra)/int(milha))

    return ("%.2f" % palavra)

def RecarregarPagina():
    navegador.refresh()
    return

def cotar():
    global acesso
    RealizarCotacao('smiles',1)
    NovaCotacao()
    acesso = acesso + 1
    sleep(2)
    RealizarCotacao('latam',2)
    NovaCotacao()
    acesso = acesso + 1
    sleep(2)
    RealizarCotacao('tudo azul',3)
    RecarregarPagina()
    sleep(5)
    NovaCotacao()
    acesso=1
    return

def main():
    print('iniciando')
    LogarSite()
    sleep(1)
    schedule.every().day.at("08:00").do(cotar)
    schedule.every().day.at("12:00").do(cotar)
    schedule.every().day.at("18:00").do(cotar)

    while 1:
        schedule.run_pending()
        time.sleep(1)
        print('Aguardando...')

if __name__ == '__main__':
   main()
