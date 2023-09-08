import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from funciones_pat.scraper import funciones_globales
from selenium.webdriver.common.action_chains import ActionChains

import os
from dotenv import load_dotenv

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')


load_dotenv()

class base_test(unittest.TestCase):

    def setUp(self):
        
        # Descomentar linea siguiente para ejecución en windows
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Descomentar linea siguiente para ejecución en linux chrome y firefox
        #self.driver = webdriver.Chrome(options=chrome_options)
        #driver=webdriver.Firefox(executable_path="C:\Drivers\geckodriver.exe")

        driver = self.driver

        # codigo para permitir las descargas de archivos en headless mode
        params = {'behavior': 'allow', 'downloadPath': os.getcwd()}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)


        # este implicity contrala el time out 
        driver.implicitly_wait(60)
        driver.maximize_window()       
    
    def test1(self):
        driver = self.driver
        f = funciones_globales(driver)
        #f.login_blue(os.getenv('url_blue_line'), os.getenv('user_blueline'), os.getenv('pass_blueline'))
        #f.dte_emitidos(os.getenv('url_dte_emitidos'))
       

        f.login_extract_sii(os.getenv('url_sii'), os.getenv('rut'), os.getenv('pass_sii'))
        f.clean_cross_data()
        #f.sql_cross(os.getenv('server_sql'), os.getenv('username_sql'), os.getenv('password_sql'), os.getenv('database_sql'))
                

        #f.sql_cross()




    def tearDown(self):
        driver = self.driver
        driver.close()
        

if __name__ == '__main__':
    unittest.main()




