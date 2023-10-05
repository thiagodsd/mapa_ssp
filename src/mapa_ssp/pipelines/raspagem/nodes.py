"""
User navigation example converted to xpath:

* Ano = 2023: ``/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select/option[2]``
* Região = Capital:  ``/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[2]/div/select/option[2]``
* Município = São Paulo: ``/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[3]/div[1]/div/select/option[2]``
* Delegacia = 001º D.P. SE: ``/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[3]/div[2]/div/select/option[2]``

Buttons:

* taxa de delitos: ``//*[@id="conteudo_btnTaxa"]``
* ocorrências registradas: ``//*[@id="conteudo_btnMensal"]``
* produtividade policial: ``//*[@id="conteudo_btnPolicial"]``
* download excel: ``//*[@id="conteudo_btnExcel"]``
"""

import os
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


def download_data(initial_year_id:int, final_year_id:int, initial_station_id:int, final_station_id:int) -> bool:
    r"""This function downloads the csv files from the SSP website.

    Parameters
    ----------
    * initial_year_id : int
        initial year index
    * final_year_id : int
        final year index
    * initial_station_id : int
        initial police station index
    * final_station_id : int
        final police station index
    
    Returns
    -------
    status : bool
        download status, true if the download was successful.
    """
    status = False

    for _year_index in range(initial_year_id, final_year_id + 1):
        pwd = os.getcwd()
        dir = rf'{pwd}/data/01_raw/{_year_index}'
        os.makedirs(dir, exist_ok=True)

        perfil = webdriver.FirefoxProfile()
        perfil.set_preference("browser.download.folderList", 2)
        perfil.set_preference('browser.download.dir', dir)
        
        navegador = webdriver.Firefox(perfil)
        navegador.get('http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx')
        
        for del_ind in range(initial_station_id, final_station_id + 1): 
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select/option[{_year_index}]'))).click()
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo_ddlRegioes"]/option[2]'))).click()
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="conteudo_ddlDelegacias"]/option[{del_ind}]'))).click()
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo_btnExcel"]'))).click()
    
        navegador.close()
    
    status = True

    return status


def data_aggregation(initial_year_id:int, final_year_id:int, download_status:bool) -> pd.DataFrame:
    """
    `todo` add docstring
    """
    df = pd.DataFrame()
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


    for _year_index in range(initial_year_id_index, final_year_id_index+1):
        for (_, _, files) in os.walk(rf"Documents/github/mapa-ssp/data/01_raw/{_year_index}/"):
            for filename in sorted(files):
                if ".csv" in filename:
                    delegacia = filename.split("ProdutividadePolicial-Delegacia")[-1].replace(".csv", "").strip()                
                    ano = int()
                    data = list()
                    missing = False
                    with open(rf"Documents/github/mapa-ssp/data/01_raw/{_year_index}/{filename}", 'r', encoding="latin-1") as f:
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