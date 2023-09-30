"""
This is a boilerplate pipeline 'raspagem'
generated using Kedro 0.17.6
"""


import os
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


def baixa_csv(ano_ini:int, ano_fim:int, del_ini:int, del_fim:int) -> NoReturn:
    """
    baixa_csv
    """

    for ano_ind in range(ano_ini, ano_fim + 1): 
        pwd = os.getcwd()
        dir = rf'{pwd}/data/01_raw/{ano_ind}'
        os.makedirs(dir, exist_ok=True)

        perfil = webdriver.FirefoxProfile()
        perfil.set_preference("browser.download.folderList", 2)
        perfil.set_preference('browser.download.dir', dir)
        
        navegador = webdriver.Firefox(perfil)
        navegador.get('http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx')
        

        for del_ind in range(del_ini, del_fim + 1): 
            WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select/option[{ano_ind}]'))).click()
            WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo_ddlRegioes"]/option[2]'))).click()
            WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="conteudo_ddlDelegacias"]/option[{del_ind}]'))).click()
            WebDriverWait(navegador, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo_btnExcel"]'))).click()
    
        navegador.close()


def consolida(ano_ini:int, ano_fim:int) -> pd.DataFrame:
    """
    consolida
    """
    df = pd.DataFrame()
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


    for ano_ind in range(ano_ini_index, ano_fim_index+1):
        for (_, _, files) in os.walk(rf"Documents/github/mapa-ssp/data/01_raw/{ano_ind}/"):
            for filename in sorted(files):
                if ".csv" in filename:
                    delegacia = filename.split("ProdutividadePolicial-Delegacia")[-1].replace(".csv", "").strip()                
                    ano = int()
                    data = list()
                    missing = False
                    with open(rf"Documents/github/mapa-ssp/data/01_raw/{ano_ind}/{filename}", 'r', encoding="latin-1") as f:
                        for line in f:
                            if ";" in line:
                                data.append([i.replace("\x00", "") for i in line.rstrip().split(";")])
                            else:
                                if (len(line) > 5) and ("!" not in line):
                                    ano = line.replace("\x00", "").rstrip().replace(" ", "")
                                else:
                                    if "!" in line:
                                        missing = True
                    if missing == False:
                        df_ = pd.DataFrame(data[1:], columns=data[0]).replace("...", 0).replace("", 0)
                        df_['ano'] = ano
                        df_['delegacia'] = delegacia
                        df_[meses + ['Total']] = df_[meses + ['Total']].astype(np.float64).astype(np.int64)
                        df = pd.concat([df, df_], axis=0)

    return df