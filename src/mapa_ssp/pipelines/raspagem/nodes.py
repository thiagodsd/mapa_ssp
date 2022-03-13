"""
This is a boilerplate pipeline 'raspagem'
generated using Kedro 0.17.6
"""

import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from typing import NoReturn

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