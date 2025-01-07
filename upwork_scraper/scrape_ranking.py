from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time 
import random
import logging
import re 
import os
import json 

import pandas as pd
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 200)

from setup_environment import configure_logging, configure_driver, get_to_page 
# get_to_page(driver, url)
driver = configure_driver()
from connect_database import create_pgdatabase_engine, save_data
# save_data(df, engine, table_name, subcategory)
engine = create_pgdatabase_engine()

def extract_ranking_data(driver, page): 
    
    """
        Extract related data from the website ranking page 
        Returns: 
         (datafram): datafram of the extracted data: [key, name, page, pagerank, ranking, ciphertext]
    """
    # when the occupation subcategory is specified to the specialty level, the occupation_uid need to be handled 
    # occupation_uid=1110580755107926016 
    pagerank = 0 
    df = pd.DataFrame(columns=['uid', 'ciphertext', 'ranking', 'page', 'pagerank', 'name', 'href'])
    for f in driver.find_elements(By.CSS_SELECTOR, "article[data-test='FreelancerTile']"): #  "div[data-test='FreelancerTile']"
        uid = f.get_attribute('data-test-key')
        href = f.find_element(By.CLASS_NAME, "profile-link").get_attribute('href')
        ciphertext = re.search(r'(~[^?]+)', href).group(1)
        name = f.find_element(By.CLASS_NAME, "profile-link").text 
        pagerank += 1
        ranking = page*10 -10 + pagerank
        df.loc[len(df)] = [uid, ciphertext, ranking, page, pagerank, name, href]
    return df 

subcategory = "Recruiting and Human Resources"
ranking_base_url = "https://www.upwork.com/ab/profiles/search/?category_uid=531770282584862721&pt=independent&revenue=1&subcategory_uid=531770282601639946"

subcategory = "Data Extraction or ELT"
ranking_base_url = "https://www.upwork.com/ab/profiles/search/?category_uid=531770282580668420&pt=independent&revenue=1&subcategory_uid=531770282593251331"

if __name__ == "__main__":
    table_name = "ranking"
    before_pt, after_pt = ranking_base_url.split("&pt=")
    for i in range(0, 1000): # loop through the pages 
        page = i + 1
        ranking_url  = f"{before_pt}&page={page}&pt={after_pt}" # construct ranking url 
        get_to_page(driver, ranking_url)
        df = extract_ranking_data(driver, page)
        if df.shape[0] != 10: # when the ranking page does not loading 10 profiles 
            logging.info(f"wait to load for ranking page {page}")
            time.sleep(random.randint(20, 40))
            df = extract_ranking_data(driver, page)
            if df.shape[0] != 10:
                logging.info(f"reload and wait for ranking page {page}")
                get_to_page(driver, ranking_url)
                time.sleep(random.randint(40, 60))
                df = extract_ranking_data(driver, page)
                if df.shape[0] != 10:
                    logging.info(f"break for ranking page {page} !!!!!")
                    break

        logging.info(f"extract data from ranking page {page}")
        save_data(df, engine, table_name, subcategory)
        
        if i % 100 == 50: # pause the process  
            time.sleep(random.randint(30, 60))
        