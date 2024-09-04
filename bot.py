
# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = True
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    pasta_dir = 'dataset-covid'
    
    if not os.path.exists(pasta_dir):
        os.makedirs(pasta_dir)

    url= "https://covid.ourworldindata.org/data/owid-covid-data.csv" 
      
    nome = os.path.basename(url) #nome do arquivo
    pasta = os.path.join(pasta_dir, nome) #adiciona na pasta

    baixar = requests.get(url) 
    baixar.raise_for_status()

    with open(pasta, 'wb') as arquivo:
        arquivo.write(baixar.content)         
    print(f"Arquivo baixado e salvo em: {pasta}")
    

    
    bot.wait(3000)
    bot.stop_browser()

    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )

def gerar_grafico(file_path='owid-covid.data.csv'):
    
    pasta_graf= 'Graficos-Salvos'
    if not os.path.exists(pasta_graf):
        os.makedirs(pasta_graf)
    nome = os.path.basename(' Novas mortes') 
    pasta = os.path.join(pasta_graf, nome) 

    df= pd.read_csv('dataset-covid\owid-covid-data.csv',sep=',', encoding='utf-8')

    list = [
        'Brazil'
    ]
 
    paises = df[df['location'].isin(list)].copy()
    
    
    paises['date'] = pd.to_datetime(paises['date'])
    paises = paises.sort_values('date') 
    agrupado = paises.groupby(['location', 'date'])['new_deaths'].sum().reset_index()
    
    # Criar um gráfico de novos casos | total de mortes | total de casos
    plt.figure(figsize=(12, 8))
    for pais in list:
        dados_pais = agrupado[agrupado['location'] == pais]
        xpoints = dados_pais['date']
        ypoints = dados_pais['new_deaths']
        plt.plot(xpoints,ypoints, label= pais)
        
    plt.xlabel('Data')
    plt.ylabel('Número de  Casos')
    plt.title(' Novas Mortes')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(pasta)
    plt.show()  
        

    print(f"Arquivo baixado e salvo em: {pasta}")
    print(f"Gráfico salvo como {nome}.png")





def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
    gerar_grafico()
